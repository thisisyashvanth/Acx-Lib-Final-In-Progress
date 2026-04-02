import { Component } from '@angular/core';
import { RequestService } from '../../../services/request.service';

@Component({
  selector: 'app-hr-requests',
  templateUrl: './hr-requests.component.html',
  styleUrl: './hr-requests.component.css'
})
export class HrRequestsComponent {

  message: string = '';
  messageType: 'success' | 'error' | '' = '';

  requests: any[] = [];
  filteredRequests: any[] = [];

  selectedBook: string = 'ALL';

  loading = false;

  constructor(private requestService: RequestService) {}

  ngOnInit() {
    this.loadRequests();
  }

  showMessage(text: string, type: 'success' | 'error') {
    this.message = text;
    this.messageType = type;

    setTimeout(() => {
      this.message = '';
      this.messageType = '';
    }, 3000);
  }

  loadRequests() {
    this.loading = true;

    this.requestService.getAllRequests().subscribe({
      next: (res) => {
        // ✅ keep your preferred sorting (by ID)
        this.requests = [...res].sort(
          (a: any, b: any) => a.request_id - b.request_id
        );

        this.applyFilter();
        this.loading = false;
      },
      error: () => {
        this.showMessage('Failed to load requests', 'error');
        this.loading = false;
      }
    });
  }

  applyFilter() {
    this.filteredRequests = this.requests.filter(req => {
      const matchesBook =
        this.selectedBook === 'ALL' || req.book_name === this.selectedBook;

      const isPending = req.status === 'PENDING';

      return matchesBook && isPending;
    });
  }

  get uniqueBooks(): string[] {
    return [...new Set(this.requests.map(r => r.book_name))];
  }

  review(requestId: number, approve: boolean) {
    this.requestService.reviewRequest(requestId, approve)
      .subscribe({
        next: () => {
          this.showMessage(
            `Request ${approve ? 'approved' : 'rejected'}`,
            'success'
          );

          // ✅ IMPORTANT FIX: reload from backend
          this.loadRequests();
        },
        error: (err) => {
          this.showMessage(
            err.error?.detail || 'Action failed',
            'error'
          );
        }
      });
  }
}