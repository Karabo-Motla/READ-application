import os
import warnings
import logging
import transformers
import Levenshtein
from typing import List, Tuple
import difflib
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
from phonemizer import phonemize
import librosa
import numpy as np

#Suppress warnings and logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
warnings.filterwarnings("ignore")
transformers.logging.set_verbosity_error()
logging.basicConfig(level=logging.CRITICAL)

# Load the pre-trained model and processor
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")


def improved_phoneme_comparison(expected_text: str, recorded_phonemes: str) -> List[Tuple[str, float]]:
    """
    Compare the expected text with recorded phonemes and calculate similarity scores.

    Args:
        expected_text (str): The expected text.
        recorded_phonemes (str): The phonemes from the recorded audio.

    Returns:
        List[Tuple[str, float]]: A list of tuples containing words and their similarity scores.
    """
    expected_phonemes = phonemize(expected_text, language='en-us', backend='espeak', 
                                  strip=True, preserve_punctuation=False, with_stress=False)
    
    recorded_phonemes_list = recorded_phonemes.split()
    expected_words = expected_text.split()
    expected_word_phonemes = expected_phonemes.split() 
    word_scores = []
    
    # Use sequence matcher for better alignment
    matcher = difflib.SequenceMatcher(None, expected_phonemes.replace(' ', ''), ''.join(recorded_phonemes_list))
    
    start = 0
    for word, phonemes in zip(expected_words, expected_word_phonemes):
        expected_phoneme_list = list(phonemes.replace(' ', ''))
        end = start + len(expected_phoneme_list)
        
        # Find the corresponding segment in the recorded phonemes
        aligned_segment = get_aligned_segment(matcher, start, end)
        score = flexible_match(expected_phoneme_list, aligned_segment)
        word_scores.append((word, score))
        start = end
    
    # Handle the case where there are more recorded phonemes than expected
    if start < len(''.join(recorded_phonemes_list)):
        remaining_segment = ''.join(recorded_phonemes_list)[start:]
        if expected_words and len(word_scores) < len(expected_words):
            last_word = expected_words[-1]
            last_phonemes = list(expected_word_phonemes[-1].replace(' ', ''))
            score = flexible_match(last_phonemes, remaining_segment)
            word_scores.append((last_word, score))
    
    return word_scores

def get_aligned_segment(matcher, start, end):
    """
    Get the aligned segment from the sequence matcher.

    Args:
        matcher (difflib.SequenceMatcher): The sequence matcher object.
        start (int): The start index of the segment.
        end (int): The end index of the segment.

    Returns:
        str: The aligned segment.
    """
    blocks = matcher.get_matching_blocks()
    aligned_segment = ''
    for block in blocks:
        a, b, size = block
        if a + size > start and a < end:
            overlap_start = max(a, start)
            overlap_end = min(a + size, end)
            aligned_segment += matcher.b[b + (overlap_start - a):b + (overlap_end - a)]
    return aligned_segment

def flexible_match(expected: List[str], recorded: str) -> float:
    """
    Calculate a flexible match score between expected and recorded phonemes.

    Args:
        expected (List[str]): List of expected phonemes.
        recorded (str): String of recorded phonemes.

    Returns:
        float: The similarity score between expected and recorded phonemes.
    """
    similarity_matrix = {
        ('a', 'ɐ'): 0.9, ('i', 'ɪ'): 0.9, ('u', 'ʊ'): 0.9,
        ('e', 'ɛ'): 0.9, ('o', 'ɔ'): 0.9, ('ə', 'ʌ'): 0.9,
        ('d', 't'): 0.8, ('b', 'p'): 0.8, ('g', 'k'): 0.8,
        ('m', 'n'): 0.8, ('f', 'v'): 0.8, ('s', 'z'): 0.8,
        ('r', 'l'): 0.7, ('ʃ', 's'): 0.7, ('θ', 'f'): 0.7,
    }

    score = 0
    expected_len = len(expected)
    recorded_len = len(recorded)
    
    i, j = 0, 0
    while i < expected_len and j < recorded_len:
        if expected[i] == recorded[j]:
            score += 1
            i += 1
            j += 1
        elif (expected[i], recorded[j]) in similarity_matrix:
            score += similarity_matrix[(expected[i], recorded[j])]
            i += 1
            j += 1
        elif (recorded[j], expected[i]) in similarity_matrix:
            score += similarity_matrix[(recorded[j], expected[i])]
            i += 1
            j += 1
        else:
            # If no match or similarity, move the pointer that's further behind
            if i/expected_len < j/recorded_len:
                i += 1
            else:
                j += 1
    
    return score / max(expected_len, recorded_len)

def provide_feedback(word_scores: List[Tuple[str, float]], expected_words: List[str], threshold: float = 0.6) -> str:
    """
    Provide feedback on pronunciation based on word scores.

    Args:
        word_scores (List[Tuple[str, float]]): List of tuples containing words and their similarity scores.
        expected_words (List[str]): List of expected words.
        threshold (float, optional): Threshold for considering a word as correctly pronounced. Defaults to 0.6.

    Returns:
        str: Feedback string containing information about each word's pronunciation.
    """
    feedback = []
    scored_words = set(word for word, _ in word_scores)
    
    for word in expected_words:
        if word in scored_words:
            score = next(score for w, score in word_scores if w == word)
            if score < threshold:
                feedback.append(f"The word '{word}' may have been mispronounced (confidence: {score:.2f}).")
            else:
                feedback.append(f"The word '{word}' was pronounced correctly (confidence: {score:.2f}).")
        else:
            feedback.append(f"The word '{word}' was not detected in the recording).")
    
    return "\n".join(feedback)
