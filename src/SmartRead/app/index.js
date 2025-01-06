import "./global.css"
import { useRootNavigationState, Redirect } from 'expo-router';
import { useUser } from "./contexts/userContext";

const App = () => {
  const rootNavigationState = useRootNavigationState();
  const { user } = useUser();

  if (!rootNavigationState?.key) return null;

  return user ? <Redirect href={'/home'} /> : <Redirect href={'/login'} />;
}

export default App;