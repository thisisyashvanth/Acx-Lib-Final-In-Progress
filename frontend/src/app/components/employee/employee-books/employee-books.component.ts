import { Component } from '@angular/core';
import { RequestService } from '../../../services/request.service';
import { AuthService } from '../../../services/auth.service';
import { UserService } from '../../../services/user.service';
import { finalize } from 'rxjs';

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
  actionInProgress: Record<number, 'RENEW' | 'RETURN' | undefined> = {};

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

  hasPendingAction(book: any): boolean {
    return Array.isArray(book.pending_request_types) && book.pending_request_types.length > 0;
  }

  hasPendingRequestType(book: any, requestType: 'RENEW' | 'RETURN'): boolean {
    return Array.isArray(book.pending_request_types) && book.pending_request_types.includes(requestType);
  }

  isActionInProgress(book: any, requestType: 'RENEW' | 'RETURN'): boolean {
    return this.actionInProgress[book.borrow_id] === requestType;
  }

  isActionLocked(book: any): boolean {
    return !!this.actionInProgress[book.borrow_id] || this.hasPendingAction(book);
  }

  getPendingActionMessage(book: any): string {
    if (this.hasPendingRequestType(book, 'RETURN')) {
      return 'Return request already pending with HR.';
    }

    if (this.hasPendingRequestType(book, 'RENEW')) {
      return 'Renew request already pending with HR.';
    }

    return 'A request is already pending with HR.';
  }

  getRenewButtonLabel(book: any): string {
    if (this.isActionInProgress(book, 'RENEW')) {
      return 'Sending...';
    }

    if (this.hasPendingRequestType(book, 'RENEW')) {
      return 'Renew Pending';
    }

    if (this.hasPendingAction(book)) {
      return 'Renew Locked';
    }

    return 'Renew';
  }

  getReturnButtonLabel(book: any): string {
    if (this.isActionInProgress(book, 'RETURN')) {
      return 'Sending...';
    }

    if (this.hasPendingRequestType(book, 'RETURN')) {
      return 'Return Pending';
    }

    if (this.hasPendingAction(book)) {
      return 'Return Locked';
    }

    return 'Return';
  }

  renewBook(book: any) {
    if (this.isActionLocked(book)) {
      this.showMessage(this.getPendingActionMessage(book), 'error');
      return;
    }

    this.actionInProgress[book.borrow_id] = 'RENEW';

    this.requestService.renew(book.borrow_id).pipe(
      finalize(() => {
        delete this.actionInProgress[book.borrow_id];
      })
    ).subscribe({
      next: () => {
        this.showMessage('Renew request sent', 'success');
        this.loadBooks(); // refresh
      },
      error: (err) => {
        this.showMessage(err.error?.detail || 'Failed to renew', 'error');
      }
    });
  }

  returnBook(book: any) {
    if (this.isActionLocked(book)) {
      this.showMessage(this.getPendingActionMessage(book), 'error');
      return;
    }

    this.actionInProgress[book.borrow_id] = 'RETURN';

    this.requestService.returnBook(book.borrow_id).pipe(
      finalize(() => {
        delete this.actionInProgress[book.borrow_id];
      })
    ).subscribe({
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
