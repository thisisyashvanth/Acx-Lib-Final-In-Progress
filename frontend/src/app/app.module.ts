import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SigninComponent } from './components/common/signin/signin.component';
import { SignupComponent } from './components/common/signup/signup.component';
import { HrsignupComponent } from './components/hr/hrsignup/hrsignup.component';
import { LandingpageComponent } from './components/common/landingpage/landingpage.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { HrDashboardComponent } from './components/hr/hr-dashboard/hr-dashboard.component';
import { EmployeeDashboardComponent } from './components/employee/employee-dashboard/employee-dashboard.component';
import { UnauthorizedComponent } from './components/unauthorized/unauthorized.component';
import { HrNavbarComponent } from './components/hr/hr-navbar/hr-navbar.component';
import { EmployeeNavbarComponent } from './components/employee/employee-navbar/employee-navbar.component';
import { EmployeeGetAllBooksComponent } from './components/employee/employee-get-all-books/employee-get-all-books.component';
import { AuthInterceptor } from './interceptor/auth.interceptor';
import { HrCreateBookComponent } from './components/hr/hr-create-book/hr-create-book.component';
import { HrRequestsComponent } from './components/hr/hr-requests/hr-requests.component';
import { EmployeeBooksComponent } from './components/employee/employee-books/employee-books.component';
import { HrGetAllBooksComponent } from './components/hr/hr-get-all-books/hr-get-all-books.component';
import { HrGetBookHistoryComponent } from './components/hr/hr-get-book-history/hr-get-book-history.component';
import { HrGetAllUsersComponent } from './components/hr/hr-get-all-users/hr-get-all-users.component';
import { HrViewUserHistoryComponent } from './components/hr/hr-view-user-history/hr-view-user-history.component';
import { HrViewRequestHistoryComponent } from './components/hr/hr-view-request-history/hr-view-request-history.component';

@NgModule({
  declarations: [
    AppComponent,
    SigninComponent,
    SignupComponent,
    HrsignupComponent,
    LandingpageComponent,
    HrDashboardComponent,
    EmployeeDashboardComponent,
    UnauthorizedComponent,
    EmployeeGetAllBooksComponent,
    HrNavbarComponent,
    EmployeeNavbarComponent,
    HrCreateBookComponent,
    HrRequestsComponent,
    EmployeeBooksComponent,
    HrGetAllBooksComponent,
    HrGetBookHistoryComponent,
    HrGetAllUsersComponent,
    HrViewUserHistoryComponent,
    HrViewRequestHistoryComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
