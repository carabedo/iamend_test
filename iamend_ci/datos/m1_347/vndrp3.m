function [sigmas, esps]=vndrp3(file,I)% I en A, esp en mm, V en microvolts

fid = fopen(file);
M = textscan(fid,' %f  %f  %f %f ' , 'delimiter', ';'); % 
fclose (fid);
%
n=length(M{1,1});
C1=zeros(n,3);

C1(:,1)=M{1,1}*1e-6;
C1(:,2)=M{1,2};
C1(:,3)=M{1,3}*1e-3;
C1(:,4)=M{1,4};

C=reshape(C1(:,1),[6 n/12*2])';
C=abs(C);
esp=reshape(C1(:,3),[6 n/12*2] );
nms=reshape(C1(:,4),[6 n/12*2] );
C(:,7)=esp(1,:);
%
ra=(C(:,1)+C(:,2))/(2*I);
rb=(C(:,3)+C(:,4))/(2*I);
rap=(C(:,5)+C(:,6))/(2*I);


for i=1:length(ra)
S1(i)=VanderpauwS(ra(i),rb(i),C(i,7));
S2(i)=VanderpauwS(rap(i),rb(i),C(i,7));
end

sigmas(:,1)=(S1+S2)/2;
sigmas(:,2)=nms(1,:);
esps=C(:,7);
end
% %%
% nms={'m1' 'm1' 'm3' 'm3' 'm5' 'm5' 'm11' 'm11' 'm4' 'm4' 'm6' 'm6' 'm9' 'm9' ...
%     'm8' 'm8' 'm7' 'm7' 'm9' 'm9'  'm2' 'm2' 'm1' 'm1'};
% ns=[1 1 3 3 5 5 11 11 4 4 6 6 9 9 8 8 7 7 9 9 2 2 1 1];
% save('sigmas347', 'sigmas', 'esps','ns')
%%
