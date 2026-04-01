import { Component } from '@angular/core';
import { BookService } from '../../../services/book.service';
import { Router } from '@angular/router';
import { RequestService } from '../../../services/request.service';

@Component({
  selector: 'app-employee-get-all-books',
  templateUrl: './employee-get-all-books.component.html',
  styleUrl: './employee-get-all-books.component.css'
})
export class EmployeeGetAllBooksComponent {

  books: any[] = [];
  loading: boolean = false;
  errorMessage: string = '';

  successMessage: string = '';
  errorActionMessage: string = '';

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
        this.loading = false;
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = 'Failed to load books';
        console.error(err);
      }
    });
  }


  borrowBook(bookId: number) {
    this.requestService.borrow(bookId)
      .subscribe({
        next: (res) => {
          this.successMessage = 'Borrow Request Sent Successfully.'
          // alert('Borrow request sent');
        },
        error: (err) => {
          this.errorActionMessage = err.error?.detail || 'Borrow failed';
          // alert(err.error.detail);
        }
      });
  }

  renewBook(borrowId: number) {
    this.requestService.renew(borrowId)
      .subscribe({
        next: () => {
          this.successMessage = 'Renew Request Sent Successfully';
          // alert('Renew request sent');
        },
        error: (err) => {
          this.errorActionMessage = err.error?.detail || 'Renew Failed';
          // alert(err.error.detail);
        }
      });
  }

  returnBook(borrowId: number) {
    this.requestService.returnBook(borrowId)
      .subscribe({
        next: () => {
          this.successMessage = 'Return Request Sent Successfully';
          // alert('Return request sent');
        },
        error: (err) => {
          this.errorActionMessage = err.error?.detail || 'Return Failed';
          // alert(err.error.detail);
        }
      });
  }

  clearMessages() {
    this.successMessage = '';
    this.errorActionMessage = '';
  }
}