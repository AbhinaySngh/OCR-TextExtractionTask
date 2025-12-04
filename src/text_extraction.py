def group_lines(data):
    """
    Group OCR words into lines based on (block_num, par_num, line_num).
    Returns an ordered list of line strings.
    """
    n_boxes = len(data['text'])
    lines = {}

    for i in range(n_boxes):
        word = data['text'][i]
        conf_str = data['conf'][i]
        try:
            conf = int(conf_str)
        except ValueError:
            conf = -1

        if conf < 0 or not word.strip():
            continue

        key = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
        if key not in lines:
            lines[key] = []
        lines[key].append(word)

    ordered_lines = []
    for key in sorted(lines.keys()):
        ordered_lines.append(" ".join(lines[key]))

    return ordered_lines


def is_barcode_line(s: str) -> bool:
    """
    Heuristic for the long alphanumeric line under the barcode.
    """
    s_no_space = s.replace(" ", "")
    if len(s_no_space) < 10:
        return False

    allowed = set("0123456789._-")
    digit_count = sum(ch.isdigit() for ch in s_no_space)
    allowed_count = sum(ch in allowed for ch in s_no_space)

    digit_ratio = digit_count / len(s_no_space)
    allowed_ratio = allowed_count / len(s_no_space)

    return digit_ratio > 0.4 and allowed_ratio > 0.9  # tuned for such codes[web:53]


def find_barcode_text(lines):
    """
    Return the first line that matches barcode pattern, or None.
    """
    for line in lines:
        if is_barcode_line(line):
            return line
    return None
