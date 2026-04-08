import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../../services/user.service';
import { ExcelService } from '../../../services/excel.service';

@Component({
  selector: 'app-hr-get-all-users',
  templateUrl: './hr-get-all-users.component.html',
  styleUrl: './hr-get-all-users.component.css'
})
export class HrGetAllUsersComponent {

  searchText: string = '';
  filteredUsers: any[] = [];

  users: any[] = [];
  loading: boolean = false;
  successMessage: string = '';
  errorMessage: string = '';

  constructor(private router: Router, private userService: UserService, private excelService: ExcelService) { }

  ngOnInit(): void {
    this.getAllUsers();
  }

  getAllUsers() {
    this.loading = true;
    this.errorMessage = '';

    this.userService.getAllUsers().subscribe({
      next: (res: any) => {

        this.users = res;
        this.filteredUsers = res;
        this.loading = false;
        console.log(res);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = 'Failed to load users';
        console.error(err);
      }
    });
  }

  filterUsers() {
    const term = this.searchText.toLowerCase();

    this.filteredUsers = this.users.filter(user =>
      (user.name?.toLowerCase().includes(term)) ||
      (user.employee_id?.toString().toLowerCase().includes(term))
    );
  }

  viewHistory(userId: number) {
    this.router.navigate(['/hr-user-view-history', userId]);
  }

  downloadExcel() {
    this.excelService.exportUsers(this.filteredUsers).subscribe({
      next: (blob: Blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');

        a.href = url;
        a.download = `users_${new Date().toISOString()}.xlsx`;

        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        this.errorMessage = 'Failed to download Excel';
        console.error(err);
      }
    });
  }
}