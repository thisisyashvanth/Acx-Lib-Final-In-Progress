import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrGetAllBooksComponent } from './hr-get-all-books.component';

describe('HrGetAllBooksComponent', () => {
  let component: HrGetAllBooksComponent;
  let fixture: ComponentFixture<HrGetAllBooksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrGetAllBooksComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HrGetAllBooksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
