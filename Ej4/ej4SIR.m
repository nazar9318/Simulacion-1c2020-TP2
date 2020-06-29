%Se conoce que inicialmente el 3% de la población se encuentra infectada, 
%toda la población es susceptible de contagiarse, la tasa de transmisión =0,27, 
%y la tasa de recuperación = 0,043 

function ej4SIR()
 %% Simulacion de un modelo de epidemias SIR
  

  % Condiciones iniciales para una poblacion
  S0 = 0.97; %susceptibles
  I0 = 0.03; %infectados 3%
  R0 = 0; %recuperados
  T0 = S0 + I0 + R0; %poblacion total

  capSalud = T0*0.30 %capacidad de sistema de salud
  dias = 200 % simulamos 200 dias para ver como se comporta la enfermedad a 
             % traves del tiempo

  h = 0.1; 

  %beta = 0.125; %tasa de transmision maxima antes de saturar el sist de salud
  beta = 0.27 %tasa de transmision dada
  gamma = 0.043; %tasa de recuperacion

  [ x_RK4, t ] = RK4( @modelo_SIR,[S0,I0,R0]' , h, [0,dias] , beta, gamma);

  figure
  hold on
  grid on
  plot(t,x_RK4(1,:),'DisplayName','Susceptibles','LineWidth',2)
  plot(t,x_RK4(2,:),'DisplayName','Infectados','LineWidth',2)
  plot(t,x_RK4(3,:),'DisplayName','Recuperados','LineWidth',2)
  plot ([0 dias], [capSalud capSalud],'DisplayName','Cap. Sist Salud','LineWidth',2)
  xlabel({'tiempo'});
  ylabel({'poblacion'});
  title({'Simulación de la pandemia'});
  legend('show');

end



function [ xp ] = modelo_SIR(x, beta, gamma )
% x(1) = Susceptibles, x(2) = Infectados,  x(3) = Recuperados

  xp = zeros(3,1);
  xp(1) = -beta*x(1)*x(2);
  xp(2) = beta*x(1)*x(2) - gamma*x(2);
  xp(3) = gamma*x(2);
end


%Runge-Kutta orden 4
function [ x, t ] = RK4( f, x0, h, T , beta, gamma)
  t0 = T(1);
  tf = T(2);

  N = floor((tf-t0)/h); % Numero de pasos total
  t = zeros(1,N);
  x = zeros(3,N);

  t(1) = t0;
  x(:,1) = x0;

  for n = 2:N
      k1 = h*f(x(:,n-1),beta,gamma);
      k2 = h*f(x(:,n-1) + 0.5*k1,beta,gamma);
      k3 = h*f(x(:,n-1) + 0.5*k2,beta,gamma);
      k4 = h*f(x(:,n-1) + k3,beta,gamma);
      x(:,n) = x(:,n-1) + (1/6)*(k1 + 2*k2 + 2*k3 + k4);
      t(n) = t(n-1) + h;
  end
end