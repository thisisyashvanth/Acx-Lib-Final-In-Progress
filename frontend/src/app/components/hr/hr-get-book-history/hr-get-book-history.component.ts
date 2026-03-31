import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RequestService } from '../../../services/request.service';
import { BookService } from '../../../services/book.service';

@Component({
  selector: 'app-hr-get-book-history',
  templateUrl: './hr-get-book-history.component.html',
  styleUrl: './hr-get-book-history.component.css'
})
export class HrGetBookHistoryComponent {

  bookId!: number;
  history: any[] = [];
  loading = true;
  error = '';

  filteredHistory: any[] = [];
  searchText: string = '';

  constructor(
    private route: ActivatedRoute,
    private bookService: BookService
  ) { }

  ngOnInit(): void {
    this.bookId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadHistory();
  }

  loadHistory() {
    this.bookService.getBookHistory(this.bookId).subscribe({
      next: (res) => {
        this.history = res;
        this.filteredHistory = res;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load history';
        this.loading = false;
      }
    });
  }

  filterHistory() {
    const term = this.searchText.toLowerCase();

    this.filteredHistory = this.history.filter(record =>
      record.employee_name.toLowerCase().includes(term) ||
      record.employee_id.toLowerCase().includes(term) ||
      record.status.toLowerCase().includes(term)
    );
  }
}