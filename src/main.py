from textnode import TextType, TextNode

def main():
    dummy = TextNode("New text node!", TextType.BOLD_TEXT, "https://boot.dev")
    print(dummy)

if __name__ == "__main__":
    main()