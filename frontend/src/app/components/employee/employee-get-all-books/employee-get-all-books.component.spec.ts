import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployeeGetAllBooksComponent } from './employee-get-all-books.component';

describe('EmployeeGetAllBooksComponent', () => {
  let component: EmployeeGetAllBooksComponent;
  let fixture: ComponentFixture<EmployeeGetAllBooksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EmployeeGetAllBooksComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EmployeeGetAllBooksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
