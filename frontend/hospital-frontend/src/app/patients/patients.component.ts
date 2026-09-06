import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-patients',
  templateUrl: './patients.component.html',
  styleUrls: ['./patients.component.css']
})
export class PatientsComponent implements OnInit {
  patients: any[] = [];
  name = '';
  age: number;

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.loadPatients();
  }

  loadPatients() {
    this.api.getPatients().subscribe(data => this.patients = data);
  }

  addPatient() {
    this.api.createPatient({ name: this.name, age: this.age }).subscribe(() => {
      this.loadPatients();
      this.name = '';
      this.age = null;
    });
  }
}
