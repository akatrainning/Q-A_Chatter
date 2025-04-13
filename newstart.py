import pyfiglet


def create_hollow_art(text):
    fig = pyfiglet.Figlet(font='standard')
    ascii_art = fig.renderText(text)
    lines = ascii_art.split('\n')
    hollow_lines = []
    for line in lines:
        new_line = ""
        for i, char in enumerate(line):
            if char != ' ' and (i == 0 or line[i - 1] == ' ' or i == len(line) - 1 or line[i + 1] == ' '):
                new_line += char
            else:
                new_line += ' '
        hollow_lines.append(new_line)
    return '\n'.join(hollow_lines)


text = "SeCUvia"
hollow_art = create_hollow_art(text)
print(hollow_art)
