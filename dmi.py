import copy
import time
import os

class Dots:
    def __init__(self):
        # ascii letters in a text file read to file
        with open('data/letters.txt', 'r') as file:
            data = file.read()

        # accepted characters to be turned to string and read
        with open('data/char_list.txt', 'r') as file:
            characters = file.read()

        # splitting string from breaks into line lists
        split_data = data.split("\n")
        del split_data[-1]

        # justified in new list
        just_data = []
        for just in split_data:
            top_value = 410
            just_data.append(just.ljust(top_value))

        # global character data
        self.char_data = copy.deepcopy(just_data)

        # hold coordinates of start and end points in ascii art
        start_coord = [0]
        end_coord = []
        letters_counted = 0

        # when a space is encountered at on all lines in list (coordinates)
        # it saves the coordinates for each letter
        for let_scroll in range(top_value):
            current_char = [
            just_data[0][let_scroll], just_data[1][let_scroll],
            just_data[2][let_scroll], just_data[3][let_scroll],
            just_data[4][let_scroll], just_data[5][let_scroll]
            ]

            # if this shows up in all 6 coordinate lines, a new character
            # is assumed
            blank_line = [' ', ' ', ' ', ' ', ' ', ' ']

            # if enough letters are counted, it will end this loop as all
            # characters will be accounted for and added
            if current_char == blank_line:
                letters_counted +=1
                end_coord.append(let_scroll)
                if letters_counted == len(characters):
                    pass
                else:
                    start_coord.append(let_scroll + 1)
            else:
                pass
        end_coord.append(len(data))

        # accepted characters, start and end points are saved to the class
        self.accepted_char = list(copy.deepcopy(characters)) + [' ']
        self.start_digs = copy.deepcopy(start_coord)
        self.end_digs = copy.deepcopy(end_coord)

        # this is a lookup table will be used to call points in the above
        # lists
        self.char_key = dict((char, i) for i, char in enumerate(characters))
        del self.char_key['\n']


    # accepted characters sorted here
    def accept(self, inp):
        for test_inpt in inp:
            if test_inpt in self.accepted_char:
                pass
            else:
                # any catch cases will be put in here and user will have to
                # start again
                print('Error: ' + "'" +
                    test_inpt + "'" +
                    ' not in accepted characters!')
                break

        # saved to class
        self.final_text = inp

    def preferences(self, time, width):
        # time delay goes here
        self.time_delay = time
        # length of text scroll (horiz) goes here
        self.scroll_length = width
    def construct(self):
        # blank dot matrix to be added to
        self.dot_matrix = ['', '', '', '', '', '']
        for letter_cons in self.final_text:
            # as space is not in the list, it has a special condition
            if letter_cons == ' ':
                for space_add in range(6):
                    self.dot_matrix[space_add] +='  '
            # letters are selected with coordinates and added line by line
            # to each list in the 2D list
            else:
                for char_add in range(6):
                    current_start = \
                        self.start_digs[self.char_key[letter_cons]]
                    current_end = \
                        self.end_digs[self.char_key[letter_cons]]
                    current_text = \
                        self.char_data[char_add][current_start:current_end]
                    self.dot_matrix[char_add]+=(current_text + ' ')

    def show_display(self):
        # this centralises the text by justifying it each end by the pixels
        # chosen by the user, this will make scrolling
        total_range = self.scroll_length + len(self.dot_matrix[0])
        print(total_range)

        for mid_text in range(6):
            self.dot_matrix[mid_text] = \
                self.dot_matrix[mid_text].rjust(self.scroll_length)
            self.dot_matrix[mid_text] = \
                self.dot_matrix[mid_text].rjust(total_range)

        # loop is here, if user selects constant loop, this will repeat
        # until user exits
        for scroll_horiz in range(total_range):
            print('\033c')
            for x in range(6):
                print(
                self.dot_matrix[x] \
                [scroll_horiz:scroll_horiz+self.scroll_length])
            time.sleep(self.time_delay)


# options are chosen by the user here in the terminal and executed from class
d_matrix = Dots()
word_input = input('What do you want to say?: ')
d_matrix.accept(word_input.lower())

rows, columns = (os.popen('stty size', 'r').read().split())
columns = int(columns)

while True:
    try:
        time_sleep = float(input('Select time delay (seconds): '))
        break
    except ValueError:
        print('Error: Time must be a number in seconds.')
while True:
    try:
        width = int(input('Choose text width: '))
        if width > columns or width < 2:
            width = columns
        else:
            pass
        break
    except ValueError:
        print('Error: Pixels are measured in whole numbers (integers).')

d_matrix.preferences(time_sleep, width)

d_matrix.construct()

d_matrix.show_display()
