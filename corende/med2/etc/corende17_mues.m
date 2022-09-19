clear
close all
%%
% lectordzinorm('data21') 
% lectordzinorm('data22') 
nms={'aire' 'M1566' 'a36-2' 'M1010' 'M1022' 'M347' 'p-79'};
ps={'k-'   'b-'  'r-'  'm-' 'g-'  'k-' 'c-' };

%%
load('data21');
semilogx(f,dzicorrnorm)
legend(nms{2:end})
hold on
load('data22');
semilogx(f,dzicorrnorm)
legend(nms{2:end})
grid on
%%
load('data21');

figure
for j=1:size(dzicorrnorm,2)-1
semilogx(f,dzicorrnorm(:,j),ps{j+1})

hold on
end
legend(nms{2:end-1})
grid on
%%
load('data22');


for j=1:size(dzicorrnorm,2)-1
semilogx(f,dzicorrnorm(:,j),ps{j+1})

hold on
end
legend(nms{2:end-1})
grid on
%%
nms={'aire' 'M1566' 'a36-2' 'M1010' 'M1050' 'M347' 'p-79'};

sigmas   = [3.68  3.83 3.83 5.76 1.05 3.948]*1e6;
esps= [ 3.38 6.54 6.54 6.52 2.30 14.96 ]*1e-3; 
%
%% fiteo z1 
load('data21');
bobina='bobinamatias';
load(bobina)
sigmapatron=sigmas(6); %  78 
dpatron=esps(6); %   78 
fitpatron=fitz1(bobina,dzicorrnorm(:,6),f,sigmapatron,dpatron);
z1=fitpatron.z1;
%% fiteo mues para todo el rango 

figure
for k=1:size(dzicorrnorm,2)-1
if k>=2
k=k+1;
subplot(2,2,k-1)
mues(k)=fitmur(bobina,dzicorrnorm(:,k),f,sigmas(k),esps(k),z1,1);
grid on
title(nms{k+1})
hold on
xlabel('f[Hz]')
ylabel('Im(dZ)/Xo')
legend(' datos experimentales ',' ajuste')    
else 
subplot(2,2,k)
mues(k)=fitmur(bobina,dzicorrnorm(:,k),f,sigmas(k),esps(k),z1,1);
grid on
title(nms{k+1})
hold on
xlabel('f[Hz]')
ylabel('Im(dZ)/Xo')
legend(' datos experimentales ',' ajuste')
end    
  
end
%% graficos separados exp1 todo el ranngo

for k=1:size(dzicorrnorm,2)-1
mues(k)=fitmur(bobina,dzicorrnorm(:,k),f,sigmas(k),esps(k),z1,1,k);
grid on
title(nms{k+1}, 'FontSize', 20);
xlhand = get(gca,'xlabel');
set(xlhand,'string','f[Hz]','fontsize',14);
ylhand = get(gca,'ylabel');
set(ylhand,'string','Im(dZ)/Xo','fontsize',14);
legend({' experimental data ',' fit '},'FontSize',14)
set(gca,'fontsize',14)
fig = gcf;
set(fig,'Position',[1200 400 600 500])
print(nms{k+1},'-dpng')

end 
%%

%% para los 3 rangos
load('data21');
mues3=zeros(size(dzicorrnorm,2),3);
for k=1:size(dzicorrnorm,2)-1
mues3(k,:)=fitmur(bobina,dzicorrnorm(:,k),f,sigmas(k),esps(k),z1,3);
grid on
title(nms{k+1}, 'FontSize', 20);
xlhand = get(gca,'xlabel');
set(xlhand,'string','f[Hz]','fontsize',14);
ylhand = get(gca,'ylabel');
set(ylhand,'string','Im(dZ)/Xo','fontsize',14);
legend({' experimental data '},'FontSize',14)
set(gca,'fontsize',14)
fig = gcf;
set(fig,'Position',[1200 400 600 500])
print(nms{k+1},'-dpng')
end 



%% fiteo mues para  el rango 10 100k
load('data22');

mues10=zeros(9,size(dzicorrnorm,2));

for k=1:size(dzicorrnorm,2)
 
[mues10(:,k), frs]=fitmur(bobina,dzicorrnorm(:,k),f,sigmas(k),esps(k),z1,10);
grid on
title(nms{k+1})
xlhand = get(gca,'xlabel');
set(xlhand,'string','f[Hz]','fontsize',14);
ylhand = get(gca,'ylabel');
set(ylhand,'string','Im(dZ)/Xo','fontsize',14);
legend({' experimental data '},'FontSize',14)
set(gca,'fontsize',14)
fig = gcf;
set(fig,'Position',[1200 400 600 500])
print(nms{k+1},'-dpng')
end


%%

save('muescor','mues','mues3','mues10')
%%
csvwrite('mues.csv',mues)
csvwrite('mues3.csv',mues3')
csvwrite('mue10.csv',mues10)

%%
save my_data.out mues -ASCII