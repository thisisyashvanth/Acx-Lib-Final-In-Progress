import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrGetBookHistoryComponent } from './hr-get-book-history.component';

describe('HrGetBookHistoryComponent', () => {
  let component: HrGetBookHistoryComponent;
  let fixture: ComponentFixture<HrGetBookHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrGetBookHistoryComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HrGetBookHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
