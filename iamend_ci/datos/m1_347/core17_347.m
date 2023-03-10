clear
close all
%lectordzinorm('datacore17') 
load('datacore17'); % 1 patron80 - 12 patron78
load('sigmas347')
ms={'aire' 'p80' 'm1' 'm2' 'm3' 'm4' 'm5' 'm6' 'm7' 'm8' 'm9' 'm11' 'p78'};
figure
semilogx(f,dzicorrnorm(:,2:end-1))
grid on
%% fiteo z1 
bobina='bobinamatias';
load(bobina)
sigmapatron=0.6102*1e6; %  78 
dpatron=14.957; %   78 
fitpatron=fitz1(bobina,dzicorrnorm(:,12),f,sigmapatron,dpatron);
z1=fitpatron.z1;
%%
[ss esps]=vndrp3('347.csv',11);
a=reshape(esps,[2 11] );
b=reshape(ss(:,2),[2 11]);
esps=[a(1,:); b(1,:)];
esps=[a(1,1:10)]
%% fiteo mues

for k=1:size(dzicorrnorm,2)-2
mues(k)=fitmur(bobina,dzicorrnorm(:,k+1),f,sigmas(k),esps(k),z1,1);
grid on
title(ms{k+2})
end

%%
figure
plot(mues)
grid on

%% montecarleo

ur1=0.06e-3; %  en mm
udh=0.06e-3; %  en mm
ul0=0.23; % en % maximo std que tira el solartron
us=1.5; % en porcentaje
ud=0.06e-3; % en mm
n=100;

% mu_fit(p,f,dziucorrnorm)  p=parametros(N,r1,r2,dh,z1,d,sigma)
for m=2:11
ran=zeros(n,5);

x=[ r1 dh 0 esps(m-1) sigmas(m-1) ];
ux=[ur1 udh 0 ud sigmas(m-1)*us/100 ];


for i=1:n
    
    for j=1:5
ran(i,j)=rand*2*ux(j) - ux(j) + x(j);
    end

dziran=rand(1,length(dzicorrnorm(:,m)'))*2.*dzicorrnorm(:,m)'*ul0/100 + dzicorrnorm(:,m)';

p=[N ran(i,1) r2 ran(i,2) z1 ran(i,4) ran(i,5) ];
mufit=mu_fit(p,f,dziran');
muesm(i,m-1)=mufit.mu;

end

end

%%
load('muesmonte')

%%

figure
plot(mues,'o')
hold on
grid on
plot(muesm','x')