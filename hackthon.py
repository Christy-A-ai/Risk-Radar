import time
import random
from datetime import datetime
import smtplib

class SmartWaterSystem:
    def _init_(self):
        self.zones = {
            'residential': {'flow_rate': 50, 'pressure': 30, 'status': 'normal'},
            'commercial': {'flow_rate': 80, 'pressure': 35, 'status': 'normal'},
            'industrial': {'flow_rate': 120, 'pressure': 40, 'status': 'normal'},
            'park': {'flow_rate': 20, 'pressure': 25, 'status': 'normal'},
            'storage_tank': {'water_level': 80, 'capacity': 100}
        }
        
        self.reuse_destinations = {
            'toilet_flushing': {'demand': 10, 'supply': 0},
            'garden_irrigation': {'demand': 15, 'supply': 0},
            'car_wash': {'demand': 5, 'supply': 0},
            'cooling_system': {'demand': 20, 'supply': 0}
        }
        
        self.leak_alerts = []
        self.authorities = ['water_department@city.gov', 'maintenance_team@city.gov']
        self.flow_threshold = 0.3
        self.pressure_threshold = 0.2
        self.simulation_time = 0
        
    def simulate_normal_operation(self):
        """Simulate normal water system operation with small random variations"""
        for zone in ['residential', 'commercial', 'industrial', 'park']:
            self.zones[zone]['flow_rate'] += random.uniform(-5, 5)
            self.zones[zone]['pressure'] += random.uniform(-2, 2)
            
            self.zones[zone]['flow_rate'] = max(10, self.zones[zone]['flow_rate'])
            self.zones[zone]['pressure'] = max(15, self.zones[zone]['pressure'])
            
    def simulate_leak(self, zone, severity='small'):
        """Simulate a leak in a specific zone"""
        print(f"\n⚠️  SIMULATING {severity.upper()} LEAK IN {zone.upper()} ZONE")
        
        if severity == 'small':
            flow_increase = 0.4
            pressure_drop = 0.25
        elif severity == 'medium':
            flow_increase = 0.7
            pressure_drop = 0.4
        else:
            flow_increase = 1.2
            pressure_drop = 0.6
            
        self.zones[zone]['flow_rate'] *= (1 + flow_increase)
        self.zones[zone]['pressure'] *= (1 - pressure_drop)
        self.zones[zone]['status'] = 'leaking'
        
        return zone, severity
    
    def detect_leaks(self):
        """Detect potential leaks by monitoring flow and pressure"""
        leaks_detected = []
        
        for zone in ['residential', 'commercial', 'industrial', 'park']:
            baseline_flow = 50 if zone == 'residential' else \
                           80 if zone == 'commercial' else \
                           120 if zone == 'industrial' else 20
                           
            baseline_pressure = 30 if zone == 'residential' else \
                               35 if zone == 'commercial' else \
                               40 if zone == 'industrial' else 25
            
            current_flow = self.zones[zone]['flow_rate']
            current_pressure = self.zones[zone]['pressure']
            
            flow_ratio = current_flow / baseline_flow
            pressure_ratio = current_pressure / baseline_pressure
            
            if flow_ratio > (1 + self.flow_threshold) and pressure_ratio < (1 - self.pressure_threshold):
                if flow_ratio > 1.8:
                    severity = 'large'
                elif flow_ratio > 1.5:
                    severity = 'medium'
                else:
                    severity = 'small'
                    
                leaks_detected.append((zone, severity, current_flow, current_pressure))
                print(f"🚨 LEAK DETECTED in {zone} zone! Flow: {current_flow:.1f}L/min, Pressure: {current_pressure:.1f}psi")
                
        return leaks_detected
    
    def reroute_water(self, leak_zone, leak_severity):
        """Reroute water from leaking zone to reuse destinations"""
        print(f"\n🔄 REROUTING WATER from {leak_zone}...")
        
        if leak_severity == 'small':
            reroute_amount = 15
        elif leak_severity == 'medium':
            reroute_amount = 30
        else:
            reroute_amount = 50
            
        total_demand = sum(dest['demand'] for dest in self.reuse_destinations.values())
        
        if reroute_amount > 0:
            for destination, data in self.reuse_destinations.items():
                allocation = min(data['demand'], reroute_amount * (data['demand'] / total_demand))
                data['supply'] += allocation
                print(f"  - Allocated {allocation:.1f}L/min to {destination.replace('_', ' ')}")
                
            self.zones[leak_zone]['flow_rate'] -= reroute_amount * 0.7
            
            water_saved = reroute_amount * 0.3
            self.zones['storage_tank']['water_level'] = min(
                100, self.zones['storage_tank']['water_level'] + water_saved
            )
            print(f"  💧 Saved {water_saved:.1f}L to storage tank (now at {self.zones['storage_tank']['water_level']:.1f}%)")
            
        return reroute_amount
    
    def send_alerts(self, leak_info):
        """Send alerts to relevant authorities about the leak"""
        zone, severity, flow, pressure = leak_info
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        alert_message = {
            'timestamp': timestamp,
            'zone': zone,
            'severity': severity,
            'flow_rate': flow,
            'pressure': pressure,
            'status': 'new'
        }
        
        self.leak_alerts.append(alert_message)
        
        print(f"\n📧 ALERT SENT TO AUTHORITIES:")
        print(f"   Time: {timestamp}")
        print(f"   Zone: {zone}")
        print(f"   Severity: {severity}")
        print(f"   Flow rate: {flow:.1f}L/min")
        print(f"   Pressure: {pressure:.1f}psi")
        
        for authority in self.authorities:
            print(f"   Sent to: {authority}")
        return alert_message
    
    def display_system_status(self):
        """Display current system status"""
        print("\n" + "="*60)
        print("SMART WATER SYSTEM STATUS")
        print("="*60)
        
        print("\nZONE MONITORING:")
        for zone, data in self.zones.items():
            if zone != 'storage_tank':
                status_icon = "✅" if data['status'] == 'normal' else "🚨"
                print(f"  {zone.capitalize():12} {status_icon} Flow: {data['flow_rate']:6.1f}L/min, "
                      f"Pressure: {data['pressure']:5.1f}psi, Status: {data['status']}")
        print(f"\nSTORAGE TANK: {self.zones['storage_tank']['water_level']:.1f}% full")
        
        print("\nWATER REUSE SYSTEM:")
        for destination, data in self.reuse_destinations.items():
            utilization = (data['supply'] / data['demand'] * 100) if data['demand'] > 0 else 0
            print(f"  {destination.replace('_', ' '):20} Demand: {data['demand']:4.1f}L/min, "
                  f"Supply: {data['supply']:4.1f}L/min, Utilization: {utilization:5.1f}%")
        
        if self.leak_alerts:
            print(f"\nACTIVE ALERTS: {len(self.leak_alerts)}")
            for i, alert in enumerate(self.leak_alerts[-3:], 1):
                print(f"  {i}. {alert['timestamp']} - {alert['zone']} ({alert['severity']})")
        print("="*60)
    
    def run_simulation(self, duration=10):
        """Run the simulation for a specified duration"""
        print("🚀 STARTING SMART WATER SYSTEM SIMULATION")
        print("💧 Monitoring for leaks, rerouting water, and sending alerts")
        
        leak_introduced = False
        
        for i in range(duration):
            self.simulation_time += 1
            print(f"\n\n⏱️  TIME STEP {self.simulation_time}")
            self.simulate_normal_operation()
            
            if i == 2 and not leak_introduced:
                leak_zone, leak_severity = self.simulate_leak('residential', 'medium')
                leak_introduced = True

            leaks = self.detect_leaks()
            
            for leak in leaks:
                zone, severity, flow, pressure = leak
                rerouted_amount = self.reroute_water(zone, severity)
                self.send_alerts(leak)
                
                if rerouted_amount > 20:
                    print(f"\n🔧 SIMULATING REPAIR in {zone} zone...")
                    time.sleep(1)
                    self.zones[zone]['status'] = 'normal'
                    print(f"✅ {zone} zone repair completed, system returning to normal")
          
            self.display_system_status()
            time.sleep(2)
        
        print("\n" + "="*60)
        print("SIMULATION COMPLETE")
        print("="*60)
        
        total_water_reused = sum(data['supply'] for data in self.reuse_destinations.values())
        print(f"\n📊 SYSTEM PERFORMANCE SUMMARY:")
        print(f"   Total water rerouted for reuse: {total_water_reused:.1f}L")
        print(f"   Storage tank level: {self.zones['storage_tank']['water_level']:.1f}%")
        print(f"   Total alerts generated: {len(self.leak_alerts)}")
        
        if self.leak_alerts:
            print(f"   First alert: {self.leak_alerts[0]['timestamp']}")
            print(f"   Last alert: {self.leak_alerts[-1]['timestamp']}")

if "_SmartWaterSystem_" == "_main_":
    water_system = SmartWaterSystem()
    water_system.run_simulation(8)
