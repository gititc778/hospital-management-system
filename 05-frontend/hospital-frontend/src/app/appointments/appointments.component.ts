import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-appointments',
  templateUrl: './appointments.component.html',
  styleUrls: ['./appointments.component.css']
})
export class AppointmentsComponent implements OnInit {

  appointments: any[] = [];

  patientId: number | null = null;
  doctor: string = '';
  date: string = '';
  time: string = '';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadAppointments();
  }

  loadAppointments() {
    this.api.getAppointments().subscribe(data => {
      this.appointments = data;
    });
  }

  addAppointment() {
    const payload = {
      patient_id: this.patientId,
      doctor: this.doctor,
      date: this.date,
      time: this.time
    };

    this.api.createAppointment(payload).subscribe(() => {
      this.loadAppointments();

      // reset form
      this.patientId = null;
      this.doctor = '';
      this.date = '';
      this.time = '';
    });
  }
}
