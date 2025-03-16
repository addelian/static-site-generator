import sys

from file_utils import copy_files_recursive
from page_utils import generate_pages_recursive

def main():
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()