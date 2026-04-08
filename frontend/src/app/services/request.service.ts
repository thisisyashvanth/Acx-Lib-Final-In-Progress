import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RequestService {

  // private baseUrl = 'http://localhost:8000/request';
  private baseUrl = `${environment.apiUrl}/request`


  constructor(private http: HttpClient) { }

  borrow(book_id: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/borrow/${book_id}`, {});
  }

  renew(borrowId: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/renew/${borrowId}`, {});
  }

  returnBook(borrowId: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/return/${borrowId}`, {});
  }

  reviewRequest(requestId: number, data: any): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/${requestId}/review`,
      data
    );
  }

  getRequests(status?: string, type?: string): Observable<Request[]> {
    let params = new HttpParams();

    if (status) params = params.set('status', status);
    if (type) params = params.set('request_type', type);

    return this.http.get<Request[]>(`${this.baseUrl}/requests`, { params });
  }

  getMyRequests() {
    return this.http.get<any[]>(`${this.baseUrl}/my-requests`);
  }
}