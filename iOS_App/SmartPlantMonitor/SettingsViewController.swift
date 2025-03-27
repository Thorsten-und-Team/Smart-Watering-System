//
//  SettingsViewController.swift
//  SmartPlantMonitor
//
//  Created by Tino Schneider on 09.01.25.
//

import UIKit

class SettingsViewController: UIViewController {
    @IBOutlet weak var ipTextField: UITextField!
    @IBOutlet weak var summertimeSwitch: UISwitch!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Lade die gespeicherte IP-Adresse, falls vorhanden
        let savedIP = UserDefaults.standard.string(forKey: "IPAddress")
        ipTextField.text = savedIP
        fetchPlantSettings()
    }
    
    func saveSettings() {
        let savedIP = UserDefaults.standard.string(forKey: "IPAddress") ?? ""
        guard let url = URL(string: "http://\(savedIP)/api") else { return }

        let settings: [String: Any] = [
            "summertime": Bool(summertimeSwitch.isOn),
        ]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: settings) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Fehler beim Senden: \(error)")
            } else {
                print("Einstellungen gespeichert!")
            }
        }.resume()
    }
    
    func saveIP() {
        // Speichere die neue IP-Adresse
        if let newIP = ipTextField.text {
            UserDefaults.standard.set(newIP, forKey: "IPAddress")
            view.endEditing(true)
        }
    }
    @IBAction func saveIPAddress(_ sender: UIButton) {
        saveIP()
    }
    
    func fetchPlantSettings() {
        let savedIP = UserDefaults.standard.string(forKey: "IPAddress") ?? ""
        guard let url = URL(string: "http://\(savedIP)/api") else { return }
            
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data, error == nil else {
                print("Fehler beim Abrufen der Daten: \(error?.localizedDescription ?? "Unbekannter Fehler")")
                return
            }
            do {
                let plantData = try JSONDecoder().decode(PlantData.self, from: data)
                DispatchQueue.main.async {
                    self.summertimeSwitch.isOn = plantData.summertime
                }
            } catch {
                print("Fehler beim Dekodieren: \(error)")
            }
        }.resume()
    }
    @IBAction func resetButton(_ sender: UIButton) {
        let savedIP = UserDefaults.standard.string(forKey: "IPAddress") ?? ""
        guard let url = URL(string: "http://\(savedIP)/api") else { return }

        let settings: [String: Any] = [
            "plant1": [
                "name": "Pflanze 1",
                "threshold": 20,
                "watering_duration": 50,
            ],
            "plant2": [
                "name": "Pflanze 2",
                "threshold": 20,
                "watering_duration": 50,
            ]
        ]
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: settings) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Fehler beim Senden: \(error)")
            } else {
                print("Einstellungen gespeichert!")
            }
        }.resume()
        if let appDomain = Bundle.main.bundleIdentifier {
            UserDefaults.standard.removePersistentDomain(forName: appDomain)
        }
        ipTextField.text = ""
        summertimeSwitch.isOn = false
        saveSettings()
        let alert = UIAlertController(title: "Zurückgesetzt!", message: "Alle Daten wurden auf Werkseinstellungen zurückgesetzt.", preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
        present(alert, animated: true, completion: nil)
    }
    
    @IBAction func summertimeSwitchChange(_ sender: UISwitch) {
        saveSettings()
    }
    
    @IBAction func dismissKeyboard(_ sender: UITapGestureRecognizer) {
            view.endEditing(true) // Schließt die Tastatur für alle aktiven Textfelder
            saveIP()
    }
    
    @IBAction func EndEditing(_ sender: UITextField) {
        saveIP()
    }
    
}
