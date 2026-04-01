import { Component } from '@angular/core';
import { RequestService } from '../../../services/request.service';

@Component({
  selector: 'app-hr-view-request-history',
  templateUrl: './hr-view-request-history.component.html',
  styleUrl: './hr-view-request-history.component.css'
})
export class HrViewRequestHistoryComponent {

  requests: any[] = [];
  filteredRequests: any[] = [];

  searchText: string = '';

  loading = false;
  successMessage = '';
  errorMessage = '';

  constructor(private requestService: RequestService) { }

  ngOnInit(): void {
    this.loadRequests();
  }

  loadRequests() {
    this.loading = true;

    this.requestService.getRequests().subscribe({
      next: (data: any[]) => {

        this.requests = data
          .filter(r => r.status === 'APPROVED' || r.status === 'REJECTED')
          .map(r => ({
            id: r.request_id,
            book_title: r.book_name,
            user_name: r.employee_name,
            request_type: r.request_type,
            status: r.status,
            request_date: r.requested_at,
            return_date: r.reviewed_at,
            remarks: r.remarks
          }));

        this.filteredRequests = this.requests;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Failed to load requests';
        this.loading = false;
      }
    });
  }

  filterRequests() {
    const text = this.searchText.toLowerCase();

    this.filteredRequests = this.requests.filter(req =>
      req.book_title.toLowerCase().includes(text) ||
      req.user_name.toLowerCase().includes(text) ||
      req.status.toLowerCase().includes(text) ||
      req.request_type.toLowerCase().includes(text)
    );
  }
}