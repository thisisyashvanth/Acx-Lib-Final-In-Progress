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

  constructor(private requestService: RequestService) { }

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
        // this.requests = res;
        this.requests = [...res].sort((a: any, b: any) => a.request_id - b.request_id);
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
      return this.selectedBook === 'ALL' || req.status === this.selectedBook;
    });
  }

  review(requestId: number, approve: boolean) {
    this.requestService.reviewRequest(requestId, approve)
      .subscribe({
        next: () => {
          this.showMessage(
            `Request ${approve ? 'approved' : 'rejected'}`,
            'success'
          );

          // Update local state
          this.requests = this.requests.map(req => {
            if (req.request_id === requestId) {
              return {
                ...req,
                status: approve ? 'APPROVED' : 'REJECTED'
              };
            }
            return req;
          });

          this.applyFilter();
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
