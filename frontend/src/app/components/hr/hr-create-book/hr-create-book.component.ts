import { Component } from '@angular/core';
import { BookService } from '../../../services/book.service';

@Component({
  selector: 'app-hr-create-book',
  templateUrl: './hr-create-book.component.html',
  styleUrl: './hr-create-book.component.css'
})
export class HrCreateBookComponent {

  book = {
    title: '',
    author: '',
    isbn: '',
    category: '',
    total_copies: 0,
    available_copies: 0
  };

  message: string = '';
  error: string = '';

  constructor(private bookService: BookService) { }

  onSubmit() {
    this.message = '';
    this.error = '';

    if (this.book.available_copies > this.book.total_copies) {
      this.error = 'Available copies cannot exceed total copies';
      return;
    }

    this.bookService.addBook(this.book).subscribe({
      next: (res: any) => {
        this.message = 'Book created successfully!';
        this.resetForm();
      },
      error: (err) => {
        this.error = err.error?.detail || 'Failed to create book';
      }
    });
  }

  resetForm() {
    this.book = {
      title: '',
      author: '',
      isbn: '',
      category: '',
      total_copies: 0,
      available_copies: 0
    };
  }

}
