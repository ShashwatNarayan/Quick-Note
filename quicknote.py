import argparse
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)
NOTES_FILE = 'notes.json'


# ---------- Utilities ----------
def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, 'r') as f:
        return json.load(f)


def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=4)


def generate_note_id(notes):
    return max([n['id'] for n in notes], default=0) + 1


# ---------- Core Functions ----------
def add_note(title, content, category):
    notes = load_notes()
    new_note = {
        'id': generate_note_id(notes),
        'title': title,
        'content': content,
        'category': category,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes.append(new_note)
    save_notes(notes)
    print(Fore.GREEN + f"Note '{title}' added.")


def list_notes(category=None):
    notes = load_notes()
    if not notes:
        print(Fore.CYAN + "No notes found.")
        return

    filtered_notes = [n for n in notes if category is None or n['category'] == category]

    for note in filtered_notes:
        print(Fore.YELLOW + f"[{note['id']}] {note['title']} ({note['category']}) - {note['timestamp']}")
        print(Style.DIM + note['content'])
        print('-' * 50)


def search_notes(keyword):
    notes = load_notes()
    results = [n for n in notes if keyword.lower() in n['title'].lower() or keyword.lower() in n['content'].lower()]

    if not results:
        print(Fore.RED + f"No notes found for '{keyword}'.")
        return

    for note in results:
        print(Fore.YELLOW + f"[{note['id']}] {note['title']} ({note['category']}) - {note['timestamp']}")
        print(Style.DIM + note['content'])
        print('-' * 50)


def delete_note(note_id):
    notes = load_notes()
    new_notes = [n for n in notes if n['id'] != note_id]
    if len(notes) == len(new_notes):
        print(Fore.RED + f"No note found with ID {note_id}.")
    else:
        save_notes(new_notes)
        print(Fore.MAGENTA + f"Note {note_id} deleted.")


def clear_notes():
    save_notes([])
    print(Fore.MAGENTA + "All notes cleared.")


# ---------- CLI Entry Point ----------
def main():
    parser = argparse.ArgumentParser(description='QuickNote – Terminal Note Taker')
    subparsers = parser.add_subparsers(dest='command')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new note')
    add_parser.add_argument('title', help='Title of the note')
    add_parser.add_argument('content', help='Content of the note')
    add_parser.add_argument('--category', default='general', help='Category of the note')

    # List command
    list_parser = subparsers.add_parser('list', help='List all notes')
    list_parser.add_argument('--category', help='Filter by category')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search notes by keyword')
    search_parser.add_argument('keyword', help='Keyword to search')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a note by ID')
    delete_parser.add_argument('id', type=int)

    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Delete all notes')

    args = parser.parse_args()

    if args.command == 'add':
        add_note(args.title, args.content, args.category)
    elif args.command == 'list':
        list_notes(args.category)
    elif args.command == 'search':
        search_notes(args.keyword)
    elif args.command == 'delete':
        delete_note(args.id)
    elif args.command == 'clear':
        clear_notes()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()