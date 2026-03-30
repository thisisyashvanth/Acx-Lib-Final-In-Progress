import { Component } from '@angular/core';
import { RequestService } from '../../../services/request.service';

@Component({
  selector: 'app-hr-requests',
  templateUrl: './hr-requests.component.html',
  styleUrl: './hr-requests.component.css'
})
export class HrRequestsComponent {

  requests: any[] = [];
  loading = false;

  constructor(private requestService: RequestService) { }

  ngOnInit() {
    this.loadRequests();
  }

  loadRequests() {
    this.loading = true;

    this.requestService.getAllRequests().subscribe({
      next: (res) => {
        this.requests = res;
        this.loading = false;
      },
      error: () => {
        alert('Failed to load requests');
        this.loading = false;
      }
    });
  }

  review(requestId: number, approve: boolean) {
    this.requestService.reviewRequest(requestId, approve)
      .subscribe({
        next: () => {
          alert(`Request ${approve ? 'approved' : 'rejected'}`);
          this.loadRequests();
        },
        error: (err) => {
          alert(err.error.detail);
        }
      });
  }
}