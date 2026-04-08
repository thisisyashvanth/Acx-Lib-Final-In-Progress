import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BookService } from '../../../services/book.service';
import { ExcelService } from '../../../services/excel.service';

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
    private bookService: BookService,
    private excelService: ExcelService
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

  downloadExcel() {
    this.excelService.exportBookHistory(this.filteredHistory).subscribe({
      next: (blob: Blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');

        a.href = url;
        a.download = `book_history_${this.bookId}_${new Date().toISOString()}.xlsx`;

        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        this.error = 'Failed to download Excel';
        console.error(err);
      }
    });
  }
}
