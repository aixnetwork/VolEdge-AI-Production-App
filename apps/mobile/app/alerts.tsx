import { ScrollView, StyleSheet, Text, View } from "react-native";

const alerts = [
  ["UVIX", "VolEdge Score above 85", "Armed"],
  ["SOXL", "Breakout confirmed by volume", "Watching"],
  ["GLD", "Accuracy above 60%", "Armed"]
] as const;

export default function Alerts() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Alerts</Text>
      {alerts.map(([symbol, condition, status]) => (
        <View key={symbol} style={styles.card}>
          <Text style={styles.symbol}>{symbol}</Text>
          <Text style={styles.condition}>{condition}</Text>
          <Text style={styles.status}>{status}</Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#080b10" },
  content: { padding: 20, paddingTop: 58 },
  title: { color: "#fff", fontSize: 28, fontWeight: "900", marginBottom: 18 },
  card: { borderWidth: 1, borderColor: "#243241", borderRadius: 8, backgroundColor: "#101820", padding: 16, marginBottom: 10 },
  symbol: { color: "#fff", fontSize: 30, fontWeight: "900" },
  condition: { color: "#d9e6ef", marginTop: 4 },
  status: { color: "#34d399", fontWeight: "900", marginTop: 10 }
});
