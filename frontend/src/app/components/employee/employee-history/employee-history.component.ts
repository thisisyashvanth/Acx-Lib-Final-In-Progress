import { Component } from '@angular/core';
import { UserService } from '../../../services/user.service';
import { AuthService } from '../../../services/auth.service';
import { RequestService } from '../../../services/request.service';

@Component({
  selector: 'app-employee-history',
  templateUrl: './employee-history.component.html',
  styleUrl: './employee-history.component.css'
})
export class EmployeeHistoryComponent {

  searchText: string = '';
  filteredHistory: any[] = [];

  history: any[] = [];
  loading = false;

  message: string = '';
  messageType: 'success' | 'error' | '' = '';

  constructor(
    private requestService: RequestService,
    private authService: AuthService
  ) { }

  ngOnInit() {
    if (!this.authService.getToken()) {
      this.showMessage('User not logged in', 'error');
      return;
    }

    this.loadHistory();
  }

  loadHistory() {
    this.loading = true;

    this.requestService.getMyRequests().subscribe({
      next: (res) => {

        this.history = res;
        this.filteredHistory = res;
        this.loading = false;
      },
      error: () => {
        this.showMessage('Failed to load history', 'error');
        this.loading = false;
      }
    });
  }

  showMessage(text: string, type: 'success' | 'error') {
    this.message = text;
    this.messageType = type;

    setTimeout(() => {
      this.message = '';
      this.messageType = '';
    }, 3000);
  }

  filterHistory() {
    const text = this.searchText.toLowerCase();

    this.filteredHistory = this.history.filter((req: any) =>
      req.book_name.toLowerCase().includes(text)
    );
  }

}
