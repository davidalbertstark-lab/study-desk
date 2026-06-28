export interface User {
  id: number;

  email: string;

  full_name: string | null;

  status:
    | "WAITLISTED"
    | "ACTIVE"
    | "REJECTED"
    | "BLOCKED";

  profile_completed: boolean;
}