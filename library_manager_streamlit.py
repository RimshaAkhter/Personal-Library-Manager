import streamlit as st
import os

# Function to load library from a file
def load_library(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            books = []
            for line in file:
                title, author, year, genre, read_status = line.strip().split(',')
                books.append({
                    'Title': title,
                    'Author': author,
                    'Year': int(year),
                    'Genre': genre,
                    'Read': read_status.lower() == 'true'
                })
            return books
    else:
        return []

# Function to save library to a file
def save_library(filename, books):
    with open(filename, 'w') as file:
        for book in books:
            file.write(f"{book['Title']},{book['Author']},{book['Year']},{book['Genre']},{book['Read']}\n")
    st.success("Library saved to file.")

# Function to add a book
def add_book(books):
    title = st.text_input("Enter the book title:")
    author = st.text_input("Enter the author:")
    year = st.number_input("Enter the publication year:", min_value=0)
    genre = st.text_input("Enter the genre:")
    read_status = st.selectbox("Have you read this book?", ["Yes", "No"])

    if st.button("Add Book"):
        books.append({
            'Title': title,
            'Author': author,
            'Year': year,
            'Genre': genre,
            'Read': read_status.lower() == "yes"
        })
        st.success("Book added successfully!")

# Function to remove a book
def remove_book(books):
    title_to_remove = st.text_input("Enter the title of the book to remove:")

    if st.button("Remove Book"):
        for book in books:
            if book['Title'].lower() == title_to_remove.lower():
                books.remove(book)
                st.success(f"Book '{title_to_remove}' removed successfully!")
                return
        st.warning(f"Book '{title_to_remove}' not found.")

# Function to search for a book by title or author
def search_books(books):
    search_choice = st.selectbox("Search by:", ["Title", "Author"])

    if search_choice == "Title":
        title = st.text_input("Enter the title:")
        found_books = [book for book in books if title.lower() in book['Title'].lower()]
    elif search_choice == "Author":
        author = st.text_input("Enter the author:")
        found_books = [book for book in books if author.lower() in book['Author'].lower()]

    if found_books:
        for i, book in enumerate(found_books, 1):
            read_status = "Read" if book['Read'] else "Unread"
            st.write(f"{i}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {read_status}")
    else:
        st.warning("No matching books found.")

# Function to display all books
def display_books(books):
    if books:
        for i, book in enumerate(books, 1):
            read_status = "Read" if book['Read'] else "Unread"
            st.write(f"{i}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {read_status}")
    else:
        st.warning("No books in the library.")

# Function to display statistics
def display_statistics(books):
    total_books = len(books)
    if total_books == 0:
        st.warning("No books to show statistics.")
        return
    read_books = sum(1 for book in books if book['Read'])
    percentage_read = (read_books / total_books) * 100
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

# Main program function
def main():
    st.title("📚 Personal Library Manager")

    # Load existing library from a file
    library_file = "library.txt"
    books = load_library(library_file)

    # Create a menu for the user
    menu = ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics", "Exit"]
    choice = st.sidebar.selectbox("Choose an option", menu)

    if choice == "Add a book":
        add_book(books)
    elif choice == "Remove a book":
        remove_book(books)
    elif choice == "Search for a book":
        search_books(books)
    elif choice == "Display all books":
        display_books(books)
    elif choice == "Display statistics":
        display_statistics(books)
    elif choice == "Exit":
        save_library(library_file, books)
        st.balloons()
        st.write("Goodbye!")

if __name__ == "__main__":
    main()
