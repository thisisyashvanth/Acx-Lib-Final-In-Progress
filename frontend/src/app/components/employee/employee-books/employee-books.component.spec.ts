import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployeeBooksComponent } from './employee-books.component';

describe('EmployeeBooksComponent', () => {
  let component: EmployeeBooksComponent;
  let fixture: ComponentFixture<EmployeeBooksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EmployeeBooksComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EmployeeBooksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
