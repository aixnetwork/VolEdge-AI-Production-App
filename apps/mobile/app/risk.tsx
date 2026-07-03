import { ScrollView, StyleSheet, Text, View } from "react-native";

const risks = [
  ["Volatility Long", "42%", "High"],
  ["Semiconductor Beta", "28%", "Elevated"],
  ["Precious Metals", "18%", "Balanced"],
  ["Cash Buffer", "12%", "Available"]
] as const;

export default function Risk() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Portfolio Risk</Text>
      {risks.map(([label, value, status]) => (
        <View key={label} style={styles.card}>
          <View>
            <Text style={styles.label}>{label}</Text>
            <Text style={styles.status}>{status}</Text>
          </View>
          <Text style={styles.value}>{value}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#080b10" },
  content: { padding: 20, paddingTop: 58 },
  title: { color: "#fff", fontSize: 28, fontWeight: "900", marginBottom: 18 },
  card: { borderWidth: 1, borderColor: "#243241", borderRadius: 8, backgroundColor: "#101820", padding: 16, marginBottom: 10, flexDirection: "row", justifyContent: "space-between" },
  label: { color: "#fff", fontSize: 18, fontWeight: "800" },
  status: { color: "#8ca3b7", marginTop: 4 },
  value: { color: "#34d399", fontSize: 38, fontWeight: "900" }
});
