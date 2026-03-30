import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-hrsignup',
  templateUrl: './hrsignup.component.html',
  styleUrl: './hrsignup.component.css'
})
export class HrsignupComponent {

  signupForm: FormGroup;
  loading: boolean = false;
  errorMessage: string = '';

  constructor(
    private authService: AuthService,
    private fb: FormBuilder,
    private router: Router
  ) {
    this.signupForm = this.fb.group({
      employeeId: ['', Validators.required],
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  onSubmit() {
    if (this.signupForm.invalid) return;

    this.loading = true;
    this.errorMessage = '';

    const payload = {
      employee_id: this.signupForm.value.employeeId,
      name: this.signupForm.value.name,
      email: this.signupForm.value.email,
      password: this.signupForm.value.password
    };

    this.authService.hrsignup(payload)
      .subscribe({
        next: (res: any) => {
          console.log('Signup Success: ', res);
          this.loading = false;
          this.router.navigate(['/signin']);
        },
        error: (err) => {
          this.loading = false;
          console.log(err.error);

          if (err.status === 400) {
            this.errorMessage = 'User Already Exists';
          } else {
            this.errorMessage = 'Something Went Wrong';
          }
        }
      });
  }
}