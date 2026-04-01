import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RequestService } from '../../../services/request.service';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-hr-view-user-history',
  templateUrl: './hr-view-user-history.component.html',
  styleUrl: './hr-view-user-history.component.css'
})
export class HrViewUserHistoryComponent {

  userId!: number;
  history: any[] = [];
  loading: boolean = false;
  errorMessage: string = '';

  searchText: string = '';
  filteredHistory: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private userService: UserService
  ) { }

  ngOnInit(): void {
    this.userId = Number(this.route.snapshot.paramMap.get('id'));
    this.getUserHistory();
  }

  getUserHistory() {
    this.loading = true;

    // 🔹 Replace with your API
    this.userService.getUserHistory(this.userId).subscribe({
      next: (res: any) => {
        this.history = res;
        this.filteredHistory = res;
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = 'Failed to load history';
        this.loading = false;
      }
    });
  }

  filterHistory() {
    const term = this.searchText.toLowerCase();

    this.filteredHistory = this.history.filter(item =>
      item.book?.title?.toLowerCase().includes(term) ||
      item.book?.author?.toLowerCase().includes(term) ||
      item.book?.category?.toLowerCase().includes(term)
    );
  }

}
