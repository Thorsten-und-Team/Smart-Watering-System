//
//  Plant2ViewController.swift
//  SmartPlantMonitor
//
//  Created by Tino Schneider on 11.01.25.
//

import UIKit

class Plant2ViewController: UIViewController {
    @IBOutlet weak var nameTextField: UITextField!
    @IBOutlet weak var humidityLabel: UILabel!
    @IBOutlet weak var lastwateredLabel: UILabel!
    @IBOutlet weak var thresholdTextField: UITextField!
    @IBOutlet weak var durationTextField: UITextField!
    
    var plantID: Int = 2 // 1 für Pflanze 1, 2 für Pflanze 2
    
    override func viewDidLoad() {
        super.viewDidLoad()
        fetchPlantSettings()
    }
    
    func fetchPlantSettings() {
        let savedIP = UserDefaults.standard.string(forKey: "IPAddress") ?? ""
        guard let url = URL(string: "http://\(savedIP)/api") else { return }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data else { return }
            do {
                let plantData = try JSONDecoder().decode(PlantData.self, from: data)
                DispatchQueue.main.async {
                    if self.plantID == 1 {
                        self.nameTextField.text = plantData.plant1.name
                        self.humidityLabel.text = "\(plantData.plant1.humidity)%"
                        self.lastwateredLabel.text = "\(plantData.plant1.last_watered)"
                        self.durationTextField.text = String(plantData.plant1.watering_duration)
                        self.thresholdTextField.text = String(plantData.plant1.threshold)
                    } else {
                        self.nameTextField.text = plantData.plant2.name
                        self.humidityLabel.text = "\(plantData.plant2.humidity)%"
                        self.lastwateredLabel.text = "\(plantData.plant2.last_watered)"
                        self.thresholdTextField.text = String(plantData.plant2.threshold)
                        self.durationTextField.text = String(plantData.plant2.watering_duration)
                    }
                }
            } catch {
                print("Fehler beim Dekodieren: \(error)")
            }
        }.resume()
    }
    
    
    func save() {
        let savedIP = UserDefaults.standard.string(forKey: "IPAddress") ?? ""
        guard let url = URL(string: "http://\(savedIP)/api") else { return }
        
        let plantKey = plantID == 1 ? "plant1" : "plant2"
        let settings: [String: Any] = [
            plantKey: [
                "name": nameTextField.text ?? "Pflanze 2",
                "threshold": Int(thresholdTextField.text ?? "") ?? 20,
                "watering_duration": Int(durationTextField.text ?? "") ?? 50,
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
    }
    
    @IBAction func dismissKeyboard(_ sender: UITapGestureRecognizer) {
        view.endEditing(true) // Schließt die Tastatur für alle aktiven Textfelder
        save()
    }
    
    @IBAction func saveSettings(_ sender: UIButton) {
        view.endEditing(true) // Schließt die Tastatur für alle aktiven Textfelder
        save()
        }
    
    @IBAction func watering(_ sender: UIButton) {
        let savedIP = UserDefaults.standard.string(forKey: "IPAddress") ?? ""
        guard let url = URL(string: "http://\(savedIP)/api") else { return }
        
        let settings: [String: Any] = [
            "watering": [
                "plant": 2
            ]
        ]
        
        let alert = UIAlertController(title: "Bewäserung gestartet!", message: "Pflanze wird jezt mit der eingestellten Wassermenge bewässert", preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
        present(alert, animated: true, completion: nil)
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: settings) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Fehler beim Senden: \(error)")
            } else {
                print("Befehl gesendet!")
            }
        }.resume()
    }
    
    }

