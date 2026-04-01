import { Component } from '@angular/core';
import { RequestService } from '../../../services/request.service';
import { AuthService } from '../../../services/auth.service';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-employee-books',
  templateUrl: './employee-books.component.html',
  styleUrl: './employee-books.component.css'
})
export class EmployeeBooksComponent {

  message: string = '';
  messageType: 'success' | 'error' | '' = '';

  books: any[] = [];
  loading = false;

  constructor(
    private requestService: RequestService,
    private authService: AuthService,
    private userService: UserService
  ) { }

  ngOnInit() {
    if (!this.authService.getToken()) {
      this.showMessage('User not logged in', 'error');
      return;
    }

    this.loadBooks();
  }

  showMessage(text: string, type: 'success' | 'error') {
    this.message = text;
    this.messageType = type;

    setTimeout(() => {
      this.message = '';
      this.messageType = '';
    }, 3000);
  }

  loadBooks() {
    this.loading = true;

    this.userService.getMyBooks().subscribe({
      next: (res) => {
        this.books = res;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.showMessage('Failed to load books', 'error');
        this.loading = false;
      }
    });
  }

  renewBook(borrowId: number) {
    this.requestService.renew(borrowId).subscribe({
      next: () => {
        this.showMessage('Renew request sent', 'success');
        this.loadBooks(); // refresh
      },
      error: (err) => {
        this.showMessage(err.error?.detail || 'Failed to renew', 'error');
      }
    });
  }

  returnBook(borrowId: number) {
    this.requestService.returnBook(borrowId).subscribe({
      next: () => {
        this.showMessage('Return request sent', 'success');
        this.loadBooks(); // refresh
      },
      error: (err) => {
        this.showMessage(err.error?.detail || 'Failed to return book', 'error');
      }
    });
  }
}