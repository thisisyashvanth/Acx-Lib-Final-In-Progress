import { Component } from '@angular/core';
import { BookService } from '../../../services/book.service';
import { Router } from '@angular/router';
import { RequestService } from '../../../services/request.service';

@Component({
  selector: 'app-hr-get-all-books',
  templateUrl: './hr-get-all-books.component.html',
  styleUrl: './hr-get-all-books.component.css'
})
export class HrGetAllBooksComponent {

  message: string = '';
  messageType: 'success' | 'error' | '' = '';

  books: any[] = [];
  loading: boolean = false;
  errorMessage: string = '';

  filteredBooks: any[] = [];
  searchText: string = '';

  constructor(private bookService: BookService, private router: Router, private requestService: RequestService) { }

  ngOnInit(): void {
    this.getAllBooks();
  }

  getAllBooks() {
    this.loading = true;
    this.errorMessage = '';

    this.bookService.getAllBooks().subscribe({
      next: (res: any) => {
        this.books = res;
        this.filteredBooks = res;
        this.loading = false;
        console.log(res);

      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = 'Failed to load books';
        console.error(err);
      }
    });
  }

  filterBooks() {
    const term = this.searchText.toLowerCase();

    this.filteredBooks = this.books.filter(book =>
      book.title.toLowerCase().includes(term) ||
      book.author.toLowerCase().includes(term) ||
      book.isbn.toLowerCase().includes(term) ||
      book.category?.toLowerCase().includes(term) ||
      book.bookNumber?.toString().toLowerCase().includes(term)
    );
  }


  borrowBook(bookId: number) {
    this.requestService.borrow(bookId).subscribe({
      next: () => {
        this.message = 'Borrow request sent successfully';
        this.messageType = 'success';
      },
      error: (err) => {
        this.message = err.error.detail || 'Failed to send borrow request';
        this.messageType = 'error';
      }
    });
  }

  renewBook(borrowId: number) {
    this.requestService.renew(borrowId).subscribe({
      next: () => {
        this.message = 'Renew request sent successfully';
        this.messageType = 'success';
      },
      error: (err) => {
        this.message = err.error.detail || 'Failed to renew';
        this.messageType = 'error';
      }
    });
  }

  returnBook(borrowId: number) {
    this.requestService.returnBook(borrowId).subscribe({
      next: () => {
        this.message = 'Return request sent successfully';
        this.messageType = 'success';
      },
      error: (err) => {
        this.message = err.error.detail || 'Failed to return book';
        this.messageType = 'error';
      }
    });
  }

  viewHistory(bookId: number) {
    this.router.navigate([`/books/${bookId}/history`]);
  }

}
