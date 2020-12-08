import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BusquedaComponent } from './busqueda/busqueda.component';
import { InicioComponent } from './components/inicio/inicio.component';

const routes: Routes = [
  { path: '', component: InicioComponent },
  { path: 'busqueda', component: BusquedaComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
