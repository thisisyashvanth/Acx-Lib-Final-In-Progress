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

  selectedType: string = 'ALL';
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

    this.requestService.getRequests().subscribe({
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
      const matchesType =
        this.selectedType === 'ALL' || req.request_type === this.selectedType;

      const isPending = req.status === 'PENDING';

      return matchesType && isPending;
    });
  }

  review(req: any, approve: boolean) {

    if (!approve && !req.remarkInput) {
      this.showMessage('Remarks required for rejection', 'error');
      return;
    }

    const payload = {
      approve: approve,
      remarks: req.remarkInput || null
    };

    this.requestService.reviewRequest(req.request_id, payload)
      .subscribe({
        next: () => {
          this.showMessage(
            `Request ${approve ? 'approved' : 'rejected'}`,
            'success'
          );
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