#################################################################
# FILE : hangman.py
# WRITER : Abed EL Rahman Nairoukh , aboudnairoukh , 213668700
# EXERCISE : intro2cs2 ex4 2022
# DESCRIPTION : a HANGMAN game
#################################################################
import hangman_helper


def update_word_pattern(word, pattern, letter):
    """This function updates the pattern of the given word"""
    new_pattern = list(pattern)
    for i in range(len(word)):
        if word[i] == letter:
            new_pattern[i] = letter
    return ''.join(new_pattern)


def letter(player_input, random_word, pattern, wrong_guess_lst, score, msg):
    """This function represent the actions when a letter is the input"""
    guessed_letter = player_input[1]
    if len(guessed_letter) > 1 or ord(guessed_letter) < 97 or \
            ord(guessed_letter) > 122:
        msg = 'The input is not a valid letter'
    elif guessed_letter in wrong_guess_lst or guessed_letter in pattern:
        msg = 'This letter was guessed already'
    else:
        score -= 1
        if guessed_letter in random_word:
            pattern = update_word_pattern(random_word, pattern, guessed_letter)
            n = random_word.count(guessed_letter)
            score += (n * (n + 1)) // 2
            msg = 'Good job! this letter is in the word'
        else:
            wrong_guess_lst.append(guessed_letter)
            msg = 'This letter is not in the word'
    return pattern, score, msg


def word(player_input, random_word, pattern, score, msg):
    """This function represent the actions when a word is the input"""
    score -= 1
    guessed_word = player_input[1]
    if guessed_word == random_word:
        n = pattern.count('_')
        score += (n * (n + 1)) // 2
        pattern = random_word
        return pattern, score, msg
    else:
        msg = "The word is incorrect"
        return pattern, score, msg


def filter_words_list(words, pattern, wrong_guess_lst):
    """This function filters the given list for hints"""
    filtered_list = []
    for current_word in words:
        suitable = True
        if len(current_word) != len(pattern):
            continue
        for i in range(len(current_word)):
            if current_word[i] in wrong_guess_lst:
                suitable = False
            if current_word[i] in pattern and current_word[i] != pattern[i]:
                suitable = False
            if pattern[i] != '_' and current_word[i] != pattern[i]:
                suitable = False
        if suitable:
            filtered_list.append(current_word)
    return filtered_list


def hint(words_list, pattern, wrong_guess_lst):
    """This function represent the actions when a hint is the input"""
    filtered_list = filter_words_list(words_list, pattern,
                                      wrong_guess_lst)
    if hangman_helper.HINT_LENGTH < len(filtered_list):
        n = len(filtered_list)
        filtered_list = [filtered_list[i * n //
                                       hangman_helper.HINT_LENGTH]
                         for i in range(hangman_helper.HINT_LENGTH)]
        hangman_helper.show_suggestions(filtered_list)
    else:
        hangman_helper.show_suggestions(filtered_list)


def run_single_game(words_list, score):
    """This function runs a single game"""
    random_word = hangman_helper.get_random_word(words_list)
    pattern = '_' * len(random_word)
    wrong_guess_lst = []
    msg = 'Hello! lets play a single game'
    while pattern != random_word and score > 0:
        hangman_helper.display_state(pattern, wrong_guess_lst, score, msg)
        player_input = hangman_helper.get_input()
        if player_input[0] == hangman_helper.LETTER:
            pattern, score, msg = letter(player_input, random_word, pattern,
                                         wrong_guess_lst, score, msg)
        elif player_input[0] == hangman_helper.WORD:
            pattern, score, msg = word(player_input, random_word, pattern,
                                       score, msg)
        elif player_input[0] == hangman_helper.HINT:
            score -= 1
            hint(words_list, pattern, wrong_guess_lst)
            msg = "Here is the hint"
    if score == 0:
        msg = "You couldn't guess the word, the chosen word was " + random_word
        hangman_helper.display_state(pattern, wrong_guess_lst, score, msg)
    else:
        msg = 'You guessed the word, good job!'
        hangman_helper.display_state(pattern, wrong_guess_lst, score, msg)
    return score


def main():
    """The main function"""
    words_lst = hangman_helper.load_words()
    score = hangman_helper.POINTS_INITIAL
    games_played = 0
    play_again = True
    while play_again:
        games_played += 1
        score = run_single_game(words_lst, score)
        if score > 0:
            msg = 'You played ' + str(games_played) + ' games. ' \
                                                      'your score is ' + \
                  str(score) + '. do you want to play another round?'
            play_again = hangman_helper.play_again(msg)
        else:
            msg = 'You played ' + str(games_played) + ' games. ' \
                                                      'your score is ' + \
                  str(score) + '. do you want to play again?'
            play_again = hangman_helper.play_again(msg)
            score = hangman_helper.POINTS_INITIAL
            games_played = 0


if __name__ == "__main__":
    #main()
    run_single_game(['fgg'], 2)