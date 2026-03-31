import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookService {

  private baseUrl = 'http://localhost:8000/books';

  constructor(private http: HttpClient) { }

  getAllBooks(): Observable<any> {
    return this.http.get(`${this.baseUrl}/get-all`);
  }

  addBook(req: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/add`, req);
  }

  getBookHistory(bookId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/${bookId}/users`);
  }

  // hrsignup(req: any) {
  //   return this.http.post(`${this.baseUrl}/hr-signup`, req);
  // }
}
