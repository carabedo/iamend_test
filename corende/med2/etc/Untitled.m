%error en Z

%%
m=6;
load('data21');

% figure
% semilogx(f,reshape(datafull{1,m}(:,4,:),[31 10])./repmat(w,[1 10]))
% grid on
% title('Re(dZ)')
figure
semilogx(f,reshape(datafull{1,m}(:,5,:),[31 10])./repmat(w,[1 10]),'k')
grid on
title('Im(dZ)')

hold on
load('data22');
%

% figure
% semilogx(f,reshape(datafull{1,m}(:,4,:),[31 10])./repmat(w,[1 10]))
% grid on
% title('Re(dZ)')

semilogx(f,reshape(datafull{1,m}(:,5,:),[size(datafull{1,m}(:,5,:),1) size(datafull{1,m}(:,5,:),3)])./repmat(w,[1 10]),'r')
grid on
title('Im(dZ)')