import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SigninComponent } from './components/common/signin/signin.component';
import { SignupComponent } from './components/common/signup/signup.component';
import { LandingpageComponent } from './components/common/landingpage/landingpage.component';
import { HrsignupComponent } from './components/hr/hrsignup/hrsignup.component';
import { EmployeeDashboardComponent } from './components/employee/employee-dashboard/employee-dashboard.component';
import { HrDashboardComponent } from './components/hr/hr-dashboard/hr-dashboard.component';
import { UnauthorizedComponent } from './components/unauthorized/unauthorized.component';
import { roleGuard } from './guards/role.guard';
import { EmployeeGetAllBooksComponent } from './components/employee/employee-get-all-books/employee-get-all-books.component';
import { HrCreateBookComponent } from './components/hr/hr-create-book/hr-create-book.component';
import { HrRequestsComponent } from './components/hr/hr-requests/hr-requests.component';
import { EmployeeBooksComponent } from './components/employee/employee-books/employee-books.component';
import { HrGetAllBooksComponent } from './components/hr/hr-get-all-books/hr-get-all-books.component';
import { HrGetBookHistoryComponent } from './components/hr/hr-get-book-history/hr-get-book-history.component';
import { HrGetAllUsersComponent } from './components/hr/hr-get-all-users/hr-get-all-users.component';
import { HrViewUserHistoryComponent } from './components/hr/hr-view-user-history/hr-view-user-history.component';
import { HrViewRequestHistoryComponent } from './components/hr/hr-view-request-history/hr-view-request-history.component';
import { EmployeeHistoryComponent } from './components/employee/employee-history/employee-history.component';

const routes: Routes = [
  { path: '', component: LandingpageComponent },
  { path: 'signin', component: SigninComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'hr-signup', component: HrsignupComponent },
  { path: 'unauthorized', component: UnauthorizedComponent },

  { path: 'employee-dashboard', component: EmployeeDashboardComponent },
  { path: 'get-all-books', component: EmployeeGetAllBooksComponent },
  { path: 'my-books', component: EmployeeBooksComponent },
  { path: 'employee-history', component: EmployeeHistoryComponent },

  { path: 'hr-dashboard', component: HrDashboardComponent, canActivate: [roleGuard] },
  { path: 'add-book', component: HrCreateBookComponent, canActivate: [roleGuard] },
  { path: 'view-requests', component: HrRequestsComponent, canActivate: [roleGuard] },
  { path: 'books/:id/history', component: HrGetBookHistoryComponent, canActivate: [roleGuard] },
  { path: 'hr-get-all-books', component: HrGetAllBooksComponent, canActivate: [roleGuard] },
  { path: 'hr-get-all-users', component: HrGetAllUsersComponent, canActivate: [roleGuard] },
  { path: 'hr-user-view-history/:id', component: HrViewUserHistoryComponent, canActivate: [roleGuard] },
  { path: 'hr-user-request-history', component: HrViewRequestHistoryComponent, canActivate: [roleGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
