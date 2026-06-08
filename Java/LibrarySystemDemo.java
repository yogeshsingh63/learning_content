package Java;

import java.util.*;
import java.util.stream.Collectors;

/**
 * LibrarySystemDemo
 * A fully-implemented demonstration class to showcase Java OOP, records, 
 * interfaces, custom exceptions, lambda expressions, and Streams.
 */
public class LibrarySystemDemo {

    // 1. Define a Record (Java 16+) for immutable Book data
    public record Book(String isbn, String title, String author, int yearPublished) implements Comparable<Book> {
        // Compact constructor for validation
        public Book {
            Objects.requireNonNull(isbn, "ISBN cannot be null");
            Objects.requireNonNull(title, "Title cannot be null");
            if (yearPublished > 2026) {
                throw new IllegalArgumentException("Publication year cannot be in the future");
            }
        }

        @Override
        public int compareTo(Book other) {
            return this.title.compareToIgnoreCase(other.title);
        }
    }

    // 2. Custom Exception
    public static class BookNotFoundException extends Exception {
        public BookNotFoundException(String message) {
            super(message);
        }
    }

    // 3. Interface defining Library Operations
    public interface Library {
        void addBook(Book book);
        void removeBook(String isbn) throws BookNotFoundException;
        List<Book> searchByAuthor(String author);
        Optional<Book> findByIsbn(String isbn);
        List<Book> getBooksSortedByTitle();
        void printInventorySummary();
    }

    // 4. Concrete implementation of the Library interface
    public static class SimpleLibrary implements Library {
        private final Map<String, Book> inventory = new HashMap<>();

        @Override
        public void addBook(Book book) {
            Objects.requireNonNull(book, "Cannot add a null book");
            inventory.put(book.isbn(), book);
            System.out.println("Added: " + book.title() + " by " + book.author());
        }

        @Override
        public void removeBook(String isbn) throws BookNotFoundException {
            if (!inventory.containsKey(isbn)) {
                throw new BookNotFoundException("No book found with ISBN: " + isbn);
            }
            Book removed = inventory.remove(isbn);
            System.out.println("Removed: " + removed.title());
        }

        @Override
        public List<Book> searchByAuthor(String author) {
            return inventory.values().stream()
                    .filter(book -> book.author().toLowerCase().contains(author.toLowerCase()))
                    .collect(Collectors.toList());
        }

        @Override
        public Optional<Book> findByIsbn(String isbn) {
            return Optional.ofNullable(inventory.get(isbn));
        }

        @Override
        public List<Book> getBooksSortedByTitle() {
            return inventory.values().stream()
                    .sorted() // Uses Book's compareTo (natural order by title)
                    .collect(Collectors.toList());
        }

        @Override
        public void printInventorySummary() {
            long count = inventory.size();
            System.out.println("\n--- Library Inventory Summary (" + count + " items) ---");
            
            // Group books by author using stream collectors
            Map<String, List<Book>> booksByAuthor = inventory.values().stream()
                    .collect(Collectors.groupingBy(Book::author));

            booksByAuthor.forEach((author, books) -> {
                System.out.println("Author: " + author);
                books.forEach(b -> System.out.println("  - [" + b.isbn() + "] " + b.title() + " (" + b.yearPublished() + ")"));
            });
            System.out.println("--------------------------------------------------\n");
        }
    }

    // 5. Main Execution Method
    public static void main(String[] args) {
        Library library = new SimpleLibrary();

        System.out.println("=== Initializing Library ===");
        library.addBook(new Book("978-0134685991", "Effective Java", "Joshua Bloch", 2018));
        library.addBook(new Book("978-0596009205", "Head First Design Patterns", "Eric Freeman", 2004));
        library.addBook(new Book("978-0132350884", "Clean Code", "Robert C. Martin", 2008));
        library.addBook(new Book("978-0137081073", "Clean Coder", "Robert C. Martin", 2011));

        // Display inventory
        library.printInventorySummary();

        // Search for books by author using streams
        System.out.println("=== Searching for books by 'Martin' ===");
        List<Book> martinBooks = library.searchByAuthor("Martin");
        martinBooks.forEach(b -> System.out.println("Found: " + b.title()));
        System.out.println();

        // Lookup book by ISBN
        String searchIsbn = "978-0134685991";
        System.out.println("=== Lookup by ISBN: " + searchIsbn + " ===");
        library.findByIsbn(searchIsbn)
                .ifPresentOrElse(
                    book -> System.out.println("Match found: " + book.title() + " (" + book.yearPublished() + ")"),
                    () -> System.out.println("Book not found")
                );
        System.out.println();

        // Sort books alphabetically by title
        System.out.println("=== Sorted Books Listing ===");
        List<Book> sortedList = library.getBooksSortedByTitle();
        sortedList.forEach(b -> System.out.println(b.title()));
        System.out.println();

        // Try removing a book and catching custom exceptions
        System.out.println("=== Removing Books ===");
        try {
            library.removeBook("978-0596009205"); // Head First Design Patterns
            library.removeBook("non-existent-isbn"); // Should throw exception
        } catch (BookNotFoundException e) {
            System.err.println("Exception caught: " + e.getMessage());
        }

        // Final inventory check
        library.printInventorySummary();
    }
}
