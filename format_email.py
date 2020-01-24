import re
import random

COLORS = ["#EC7063", "#A569BD", "#5DADE2", "#52BE80", "#F4D03F", "#F5B041"]


def format_msg(msg):
    """Sanitize text and format hashtags"""

    body = ""
    hashtags = []
    # split on spaces and newlines
    for i, word in enumerate(re.split('[ \n]', msg.text)):
        if len(word) > 0 and word[0] == '#':
            hashtags.append(word)
        else:
            # get body and replace all newlines with proper markdown newlines
            # if i != 0, then there are hashtags to remove from body
            body = re.split('[ \n]', msg.text, i)[i] if i != 0 else msg.text
            body = body.replace("\n", "  \n")
            break

    # ensure markdown doesn't interpret headers
    sanitized_hashtags = [tag.replace("#", "\#") for tag in hashtags]
    # color hashtags with a random color
    colored_hashtags = [color_hashtag(tag) for tag in sanitized_hashtags]

    return "{}  \n{}".format(' '.join(colored_hashtags), body)


def format_msg_group(header, date, msgs):
    """Format a message group into markdown."""

    # format date
    date_str = date.strftime("%B %d, %Y")

    # format messages and join
    msg_str = "\n".join([format_msg(msg) + "\n" for msg in msgs])

    return f"""
### {header} - {date_str}

{msg_str}
"""


def format_email_body(snippets):
    """Format entire email from markdown snippets"""

    snippet_str = "\n".join(snippets)

    return f"""
{snippet_str}
"""


def color_hashtag(tag):
    """If tag has been seen before, color it the same. Otherwise, random."""
    color = ""
    if tag in color_hashtag.history:
        color = color_hashtag.history[tag]
    else:
        color = random.choice(COLORS)
        color_hashtag.history[tag] = color

    return f"<span style=\"color:{color}\">{tag}</span>"


color_hashtag.history = {}
