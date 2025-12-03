from manim import *
import numpy as np

# Configuración opcional para el estilo visual general
 config.background_color = "#1e1e1e" # Un fondo oscuro estilo pizarra

class Escena1_CreacionExciton(Scene):
    def construct(self):
        # 1. Crear la red cristalina (simplificada 2D)
        atoms = VGroup()
        electrons = VGroup()
        for x in range(-4, 5):
            for y in range(-2, 3):
                # Núcleos positivos (rojos)
                atom = Circle(radius=0.15, color=RED, fill_opacity=0.5).move_to(RIGHT*x + UP*y*1.2)
                atoms.add(atom)
                # Electrones de valencia (azules) sentados en los átomos
                elec = Dot(radius=0.08, color=BLUE).move_to(atom.get_center())
                electrons.add(elec)
        
        lattice = VGroup(atoms, electrons).center()
        self.play(Create(atoms), Create(electrons), run_time=2)
        self.wait(1)

        # 2. El Fotón Incidente
        # Elegimos un electrón central como objetivo
        target_electron = electrons[22] 
        target_atom = atoms[22]

        photon = Wave(
            start=LEFT*6 + UP*2,
            end=target_atom.get_center(),
            wavelength=0.5,
            amplitude=0.2,
            color=YELLOW
        )
        label_photon = Text("Fotón ($h\\nu \\ge E_g$)", font_size=24, color=YELLOW).next_to(photon.get_start(), UP)

        self.play(Create(photon), Write(label_photon), run_time=1.5)
        self.play(photon.animate.shift(RIGHT*5), run_time=1) # El fotón golpea

        # 3. Excitación: Creación del par Electrón-Hueco
        # El electrón salta y deja un hueco
        hole = Dot(radius=0.12, color=RED_E).move_to(target_atom.get_center())
        label_hole = Text("Hueco (+)", font_size=20, color=RED_E).next_to(hole, DOWN)
        
        excited_electron = target_electron.copy().set_color(BLUE_E)
        label_elec = Text("Electrón (-)", font_size=20, color=BLUE_E).next_to(excited_electron, UP)

        self.play(
            FadeOut(photon), FadeOut(label_photon),
            FadeOut(target_electron), # El electrón original desaparece
            FadeIn(hole), Write(label_hole), # Aparece el hueco
            excited_electron.animate.shift(UP*1.5 + RIGHT*0.5), # El electrón salta
            Write(label_elec)
        )
        self.wait(0.5)

        # 4. Formación del Excitón (La atracción)
        # Creamos una línea que representa la fuerza de Coulomb entre ellos
        coulomb_force = always_redraw(lambda: DashedLine(
            start=hole.get_center(),
            end=excited_electron.get_center(),
            color=PURPLE_B
        ))
        exciton_label = Text("Excitón", font_size=36, color=PURPLE).to_edge(UP)

        self.play(Create(coulomb_force), Write(exciton_label))

        # Animamos un pequeño "baile" orbital para mostrar que están ligados
        # Movemos el electrón alrededor del hueco
        orbit_path = Circle(radius=1.5).move_to(hole.get_center())
        self.play(
            MoveAlongPath(excited_electron, orbit_path),
            run_time=4,
            rate_func=linear
        )
        
        final_text = Text("Estado ligado neutro", font_size=24).next_to(exciton_label, DOWN)
        self.play(Write(final_text))
        self.wait(3)