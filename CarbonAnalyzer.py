import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

class CarbonAnalyzer:
    """Clase para analizar y visualizar datos de emisiones de carbono"""
    
    def __init__(self):
        self.arbol_joven_kg_ano = 30
        self.arbol_adulto_kg_ano = 300
        
    def analizar_emisiones_csv(self, csv_path="emissions.csv"):
        """Analiza el archivo CSV de emisiones generado por codecarbon"""
        try:
            df = pd.read_csv(csv_path)
            
            if df.empty:
                print("No hay datos de emisiones para analizar")
                return
                
            # Análisis básico
            total_emissions = df['emissions'].sum()
            total_duration = df['duration'].sum()
            avg_emissions_rate = df['emissions_rate'].mean()
            
            print(f"\n{'='*50}")
            print("ANÁLISIS DE EMISIONES HISTÓRICAS")
            print(f"{'='*50}")
            print(f"Total de ejecuciones: {len(df)}")
            print(f"Emisiones totales: {total_emissions:.6f} kg CO2eq")
            print(f"Duración total: {total_duration:.2f} segundos")
            print(f"Tasa promedio de emisiones: {avg_emissions_rate:.8f} kg CO2eq/s")
            
            # Cálculos de compensación
            self.calcular_compensacion_detallada(total_emissions, total_duration)
            
            # Generar gráficos si hay suficientes datos
            if len(df) > 1:
                self.generar_graficos(df)
                
            return df
            
        except FileNotFoundError:
            print(f"Archivo {csv_path} no encontrado")
            return None
        except Exception as e:
            print(f"Error al analizar emisiones: {e}")
            return None
    
    def calcular_compensacion_detallada(self, emissions, duration_seconds):
        """Calcula compensación detallada por árboles"""
        
        duration_hours = duration_seconds / 3600
        emissions_per_hour = emissions / duration_hours if duration_hours > 0 else 0
        
        # Horas que puede compensar cada árbol por año
        horas_joven_por_ano = self.arbol_joven_kg_ano / (emissions_per_hour * 24 * 365) if emissions_per_hour > 0 else float('inf')
        horas_adulto_por_ano = self.arbol_adulto_kg_ano / (emissions_per_hour * 24 * 365) if emissions_per_hour > 0 else float('inf')
        
        # Árboles necesarios para compensar totalmente
        arboles_jovenes_necesarios = emissions / self.arbol_joven_kg_ano
        arboles_adultos_necesarios = emissions / self.arbol_adulto_kg_ano
        
        print(f"\n{'='*50}")
        print("CÁLCULOS DE COMPENSACIÓN")
        print(f"{'='*50}")
        print(f"Emisiones por hora: {emissions_per_hour:.8f} kg CO2eq/h")
        print(f"\n🌱 ÁRBOL JOVEN (30 kg CO2/año):")
        print(f"  • Puede compensar: {horas_joven_por_ano:.0f} horas de procesamiento/año")
        print(f"  • Árboles necesarios: {arboles_jovenes_necesarios:.6f}")
        print(f"\n🌳 ÁRBOL ADULTO (300 kg CO2/año):")
        print(f"  • Puede compensar: {horas_adulto_por_ano:.0f} horas de procesamiento/año")
        print(f"  • Árboles necesarios: {arboles_adultos_necesarios:.6f}")
        
        # Contexto adicional
        print(f"\n📊 CONTEXTO:")
        print(f"  • Equivale a {emissions*1000:.3f} gramos de CO2")
        print(f"  • Equivale a {emissions/0.000411:.1f} km en auto promedio")
        print(f"  • Equivale a {emissions/0.0002:.1f} km en transporte público")
        
        return {
            'emissions_per_hour': emissions_per_hour,
            'horas_joven_ano': horas_joven_por_ano,
            'horas_adulto_ano': horas_adulto_por_ano,
            'arboles_jovenes_necesarios': arboles_jovenes_necesarios,
            'arboles_adultos_necesarios': arboles_adultos_necesarios
        }
    
    def generar_graficos(self, df):
        """Genera gráficos de análisis de emisiones"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Gráfico 1: Emisiones por ejecución
        ax1.plot(range(len(df)), df['emissions'], marker='o')
        ax1.set_title('Emisiones por Ejecución')
        ax1.set_xlabel('Número de Ejecución')
        ax1.set_ylabel('Emisiones (kg CO2eq)')
        ax1.grid(True)
        
        # Gráfico 2: Duración vs Emisiones
        ax2.scatter(df['duration'], df['emissions'])
        ax2.set_title('Duración vs Emisiones')
        ax2.set_xlabel('Duración (segundos)')
        ax2.set_ylabel('Emisiones (kg CO2eq)')
        ax2.grid(True)
        
        # Gráfico 3: Tasa de emisiones
        ax3.plot(range(len(df)), df['emissions_rate'], marker='s', color='red')
        ax3.set_title('Tasa de Emisiones')
        ax3.set_xlabel('Número de Ejecución')
        ax3.set_ylabel('Tasa (kg CO2eq/s)')
        ax3.grid(True)
        
        # Gráfico 4: Consumo de energía
        ax4.plot(range(len(df)), df['energy_consumed'], marker='^', color='green')
        ax4.set_title('Consumo de Energía')
        ax4.set_xlabel('Número de Ejecución')
        ax4.set_ylabel('Energía (kWh)')
        ax4.grid(True)
        
        plt.tight_layout()
        
        # Guardar gráfico
        os.makedirs('./carbon_analysis', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'./carbon_analysis/analisis_emisiones_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\nGráficos guardados en: ./carbon_analysis/analisis_emisiones_{timestamp}.png")

# Función para ejecutar análisis independiente
def main():
    analyzer = CarbonAnalyzer()
    analyzer.analizar_emisiones_csv("emissions.csv")

if __name__ == "__main__":
    main()