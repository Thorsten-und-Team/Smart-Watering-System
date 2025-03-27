//
//  ViewController.swift
//  SmartPlantMonitor
//
//  Created by Tino Schneider on 09.01.25.
//
struct PlantData: Codable {
    struct Plant: Codable {
        let name: String
        let humidity: Double
        let last_watered: String
        let threshold: Int
        let watering_duration: Int
    }
    let plant1: Plant
    let plant2: Plant
    let summertime: Bool
    let last_update: String
}


import UIKit

class ViewController: UIViewController {
    
    @IBOutlet weak var plant1NameLabel: UILabel!
    @IBOutlet weak var plant1HumidityLabel: UILabel!
    @IBOutlet weak var plant1LastWateredLabel: UILabel!
    @IBOutlet weak var plant1thresholdLabel: UILabel!
    @IBOutlet weak var plant1watering_durationLabel: UILabel!
    @IBOutlet weak var plant2NameLabel: UILabel!
    @IBOutlet weak var plant2HumidityLabel: UILabel!
    @IBOutlet weak var plant2LastWateredLabel: UILabel!
    @IBOutlet weak var plant2thresholdLabel: UILabel!
    @IBOutlet weak var plant2watering_durationLabel: UILabel!
    @IBOutlet weak var lastUpdateLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        fetchPlantData()
    }
    
    func fetchPlantData() {
        let savedIP = UserDefaults.standard.string(forKey: "IPAddress") ?? ""
        guard let url = URL(string: "http://\(savedIP)/api") else { return }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard let data = data, error == nil else {
                print("Fehler beim Abrufen der Daten: \(error?.localizedDescription ?? "Unbekannt")")
                return
            }

            do {
                let plantData = try JSONDecoder().decode(PlantData.self, from: data)
                DispatchQueue.main.async {
                    self.updateUI(with: plantData)
                    
                }
            } catch {
                print("Fehler beim Dekodieren der JSON-Daten: \(error.localizedDescription)")
            }
        }.resume()
    }

    
    func updateUI(with data: PlantData) {
        plant1NameLabel.text = "\(data.plant1.name)"
        plant1HumidityLabel.text = "\(data.plant1.humidity)%"
        plant1LastWateredLabel.text = "\(data.plant1.last_watered)"
        plant1thresholdLabel.text = "\(data.plant1.threshold)%"
        plant1watering_durationLabel.text = "\(data.plant1.watering_duration) ml"
        
        plant2NameLabel.text = "\(data.plant2.name)"
        plant2HumidityLabel.text = "\(data.plant2.humidity)%"
        plant2LastWateredLabel.text = "\(data.plant2.last_watered)"
        plant2thresholdLabel.text = "\(data.plant2.threshold)%"
        plant2watering_durationLabel.text = "\(data.plant2.watering_duration) ml"
        
        lastUpdateLabel.text = "zuletzt aktualisiert: \(data.last_update)"
    }

    
    @IBAction func reload(_ sender: UIButton) {
        fetchPlantData()
    }
    
    
}

