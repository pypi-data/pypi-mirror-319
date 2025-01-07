import os
from .tokenizer import KinTokenizer


def train_kin_tokenizer(text, vocab_size=276, save=False, tokenizer_path=None, retrain=False):
    """
    Function for training the tokenizer
    params:
        text: the string text that will be used for training the tokenizer
        vocab_size: the final size of the voacabulary for the tokenizer
        save: boolean to indicate if tokenizer has to be saved after training for future use
        tokenizer_path: the path to which the tokenizer will be saved if save is True
    Returns:
        returns tokenizer object after training
    """
    tokenizer = KinTokenizer()
    start_merge_iter = 0
    if retrain:
        tokenizer.load(os.path.join(tokenizer_path, "kin_tokenizer.pkl"))
        start_merge_iter = max(list(tokenizer.vocab.keys()))
    if len(text) < vocab_size or type(text) != str:
        raise ValueError("length of text should be greater or equal to vocab_size, vocab_size should be at least 256 and text should be a string")
    
    if save == True:
        if tokenizer_path is None:
           tokenizer_path = os.path.join("kin_tokenizer", "data")
        
        tokenizer.train(text, vocab_size, start_merge_iter=start_merge_iter, tokenizer_path=tokenizer_path)
        tokenizer.save(tokenizer_path)
    else:
        tokenizer.train(text, vocab_size, start_merge_iter=start_merge_iter)

    return tokenizer


def create_sequences(tokens, seq_len, step=None):
    """
    Function for creating sequences for next word prediction
    params:
        tokens: list of tokens(integers)
        seq_len: the length for each sequence to be created
    returns:
        the list of sequences(list of tokens with length of seq_len)
    """
    tokens_len = len(tokens)
    sources, targets = [], []
    if step is None:
        factor = seq_len / 1024
        step = int((seq_len * 25 / factor) / 3200)
    for i in range(tokens_len):
        i = i * step
        sequence = tokens[i: i + seq_len + 1]
        source = sequence[:-1]

        if len(source) < (seq_len * 9) // 10:
            break
        elif len(source) < seq_len:
            source += [0] * (seq_len - len(source))

        target = sequence[-1]
        sources.append(source)
        targets.append(target)
    return sources, targets



def create_sequences_batch(args):
    """ 
    Helper function to create sequences for a batch of tokens. 
    args:
        is the tuple of (tokens, seq_len, step, start_index, end_index)
        in the order listed
    """
    tokens, seq_len, step, start_index, end_index = args
    if step is None:
        factor = seq_len / 1024
        step = int((seq_len * 25 / factor) / 3200)
    sources, targets = [], []
    for i in range(start_index, end_index):
        i = i * step
        sequence = tokens[i: i + seq_len + 1]
        source = sequence[:-1]

        if len(source) < (seq_len * 9) // 10:
            break
        elif len(source) < seq_len:
            source += [0] * (seq_len - len(source))

        target = sequence[-1]
        sources.append(source)
        targets.append(target)
    return sources, targets



