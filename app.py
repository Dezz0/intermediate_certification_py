import csv
import os
from datetime import datetime

class Note:
    def __init__(self, note_id, title, body, timestamp):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.timestamp = timestamp

class NotesManager:
    def __init__(self, filename='notes.csv'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader) 
            notes = []
            for row in reader:
                note = Note(*row)
                notes.append(note)
            return notes

    def save_notes(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['ID', 'Title', 'Body', 'Timestamp'])
            for note in self.notes:
                writer.writerow([note.note_id, note.title, note.body, note.timestamp])

    def add_note(self, title, body):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        note_id = len(self.notes) + 1
        note = Note(note_id, title, body, timestamp)
        self.notes.append(note)
        self.save_notes()
        print('Заметка успешно сохранена.')

    def list_notes(self, filter_date=None):
        if filter_date:
            filtered_notes = [note for note in self.notes if note.timestamp.startswith(filter_date)]
        else:
            filtered_notes = self.notes

        if not filtered_notes:
            print('----------------------------------------------------------------------------')
            print('Список заметок пуст.')
            return

        for note in filtered_notes:
            print('----------------------------------------------------------------------------')
            print(f'ID: {note.note_id}, Заголовок: {note.title}, Дата/время: {note.timestamp}')        

    def edit_note(self, note_id, new_title, new_body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = new_title
                note.body = new_body
                note.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                print('Заметка успешно отредактирована.')
                return
        print('Заметка с указанным ID не найдена.')

    def delete_note(self, note_id):
        note_exists = False
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                note_exists = True
                break

        if note_exists:
            self.save_notes()
            print('Заметка успешно удалена.')
        else:
            print(f'Заметка с ID {note_id} не существует.')
                 
if __name__ == '__main__':
    manager = NotesManager()

    while True:
        print('\nВыберите команду:')
        print('1. Добавить заметку')
        print('2. Список заметок (с фильтрацией по дате)')
        print('3. Редактировать заметку')
        print('4. Удалить заметку')
        print('5. Выйти')
        choice = input('\nВведите номер команды: ')

        if choice == '1':
            title = input('\nВведите заголовок заметки: ')
            body = input('Введите тело заметки: ')
            manager.add_note(title, body)
        elif choice == '2':
            filter_date = input('\nВведите дату для фильтрации (гггг-мм-дд) или оставьте пустым: ')
            manager.list_notes(filter_date)
        elif choice == '3':
            note_id = int(input('\nВведите ID заметки для редактирования: '))
            new_title = input('Введите новый заголовок заметки: ')
            new_body = input('Введите новое тело заметки: ')
            manager.edit_note(note_id, new_title, new_body)
        elif choice == '4':
            note_id = int(input('\nВведите ID заметки для удаления: '))
            manager.delete_note(note_id)
        elif choice == '5':
            break
        else:
            print('\nНекорректная команда. Пожалуйста, выберите существующую команду.')
