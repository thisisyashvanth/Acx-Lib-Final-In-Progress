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

  books: any[] = [];
  loading = false;

  constructor(
    private requestService: RequestService,
    private authService: AuthService,
    private userService: UserService
  ) { }

  ngOnInit() {
    if (!this.authService.getToken()) {
      alert('User not logged in');
      return;
    }

    this.loadBooks();
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
        alert('Failed to load books');
        this.loading = false;
      }
    });
  }

  renewBook(borrowId: number) {
    this.requestService.renew(borrowId).subscribe({
      next: () => {
        alert('Renew request sent');
        this.loadBooks(); // 🔄 refresh
      },
      error: (err) => {
        alert(err.error.detail);
      }
    });
  }

  returnBook(borrowId: number) {
    this.requestService.returnBook(borrowId).subscribe({
      next: () => {
        alert('Return request sent');
        this.loadBooks(); // 🔄 refresh
      },
      error: (err) => {
        alert(err.error.detail);
      }
    });
  }
}